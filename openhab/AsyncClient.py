import aiohttp
import asyncio
from typing import Optional, Dict, Any

from .Client import StatusResponse


class AsyncOpenHABClient:
    DEFAULT_TIMEOUT = 10
    SSE_CONNECT_TIMEOUT = 10

    def __init__(
        self,
        url: str,
        username: str = None,
        password: str = None,
        token: str = None,
        timeout: float = DEFAULT_TIMEOUT,
        verify: bool = True
    ):
        """
        Initializes the asynchronous OpenHAB client.

        Use it as an asynchronous context manager::

            async with AsyncOpenHABClient(url, token=token) as client:
                items = await AsyncItems(client).getItems()

        :param url: The base URL of the openHAB server (e.g., "http://127.0.0.1:8080").
        :param username: Optional; The username for Basic Authentication.
        :param password: Optional; The password for Basic Authentication.
        :param token: Optional; The Bearer Token for Token-based Authentication.
        :param timeout: Optional; Timeout in seconds for normal requests (default is 10).
        :param verify: Optional; TLS verification (default is True).
        """
        self.url = url.rstrip("/")
        self.username = username
        self.password = password
        self.token = token
        self.timeout = timeout
        self.verify = verify

        self.auth = None
        if username and password:
            self.auth = aiohttp.BasicAuth(username, password)

        self.session: Optional[aiohttp.ClientSession] = None
        self.isCloud = False
        self.isLoggedIn = False

    async def __aenter__(self):
        """
        Async context manager start: opens the session and checks the connection.
        """
        await self._ensureSession()
        await self.__login()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Async context manager end.
        """
        await self.close()

    async def close(self):
        """Closes the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
        self.session = None

    async def _ensureSession(self):
        if self.session is None or self.session.closed:
            headers = {}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"
            connector = aiohttp.TCPConnector(ssl=None if self.verify else False)
            # No total timeout on the session – SSE streams must stay open.
            self.session = aiohttp.ClientSession(auth=self.auth, headers=headers, connector=connector,
                                                 timeout=aiohttp.ClientTimeout(total=None))
        return self.session

    async def __login(self):
        """
        Asynchronous login / connectivity check.
        """
        self.isCloud = self.url in ("https://myopenhab.org", "https://home.myopenhab.org")

        try:
            async with self.session.get(self.url + "/rest/",
                                        timeout=aiohttp.ClientTimeout(total=self.timeout)) as resp:
                resp.raise_for_status()
                self.isLoggedIn = resp.status == 200

        except aiohttp.ClientResponseError as err:
            print(f"HTTP error occurred: {err}")
        except aiohttp.ClientConnectorError as err:
            print(f"Connection error occurred: {err}")
        except asyncio.TimeoutError as err:
            print(f"Timeout occurred: {err}")
        except Exception as err:
            print(f"Request exception occurred: {err}")

    def _buildUrl(self, resourcePath: str) -> str:
        if resourcePath.startswith("http://") or resourcePath.startswith("https://"):
            return resourcePath
        if not resourcePath.startswith("/"):
            resourcePath = "/" + resourcePath
        if not (resourcePath == "/rest" or resourcePath.startswith("/rest/") or resourcePath.startswith("/rest?")):
            resourcePath = "/rest" + resourcePath
        # "#" is valid inside openHAB UIDs (channel and action UIDs), but would start a URL fragment.
        path, sep, query = resourcePath.partition("?")
        resourcePath = path.replace("#", "%23") + sep + query
        return self.url + resourcePath

    @staticmethod
    def _cleanParams(params):
        if not params:
            return None
        clean = {}
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, bool):
                value = str(value).lower()
            elif not isinstance(value, str):
                value = str(value)
            clean[key] = value
        return clean

    @staticmethod
    async def _raiseForStatus(resp: aiohttp.ClientResponse):
        """
        Raises aiohttp.ClientResponseError for 4xx/5xx and adds the error message
        that openHAB sends in the body.
        """
        if resp.status < 400:
            return
        message = resp.reason or ""
        try:
            body = await resp.json(content_type=None)
            if isinstance(body, dict) and isinstance(body.get("error"), dict) and body["error"].get("message"):
                message = f"{message} ({body['error']['message']})"
        except Exception:
            pass
        raise aiohttp.ClientResponseError(resp.request_info, resp.history, status=resp.status,
                                          message=message, headers=resp.headers)

    async def __executeRequest(
        self,
        headers: Dict = None,
        resourcePath: str = None,
        method: str = None,
        data: Any = None,
        params: Dict = None
    ):
        """
        Executes an async HTTP request.

        :return: The decoded JSON, the response text, or a StatusResponse for empty bodies.
        :raises aiohttp.ClientResponseError: For 4xx/5xx responses.
        """
        if not resourcePath or not method:
            raise ValueError("resourcePath and method must be specified!")

        method = method.lower()
        if method not in ("get", "post", "put", "delete"):
            raise ValueError("Invalid HTTP method provided!")

        session = await self._ensureSession()
        headers = {k: v for k, v in (headers or {}).items() if v is not None}
        if isinstance(data, str):
            if data and not any(k.lower() == "content-type" for k in headers):
                # openHAB rejects bodies without a matching media type (415)
                isJson = data.lstrip()[:1] in ("{", "[")
                headers["Content-Type"] = "application/json" if isJson else "text/plain"
            data = data.encode("utf-8")

        async with session.request(
            method=method,
            url=self._buildUrl(resourcePath),
            params=self._cleanParams(params),
            data=data,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as resp:
            await self._raiseForStatus(resp)

            # openHAB sends UTF-8 (e.g. "21.5 °C") without always declaring the charset
            text = await resp.text(encoding=resp.charset or "utf-8")

            if not text.strip():
                result = StatusResponse(status=resp.status)
                if resp.headers.get("Location"):
                    result["location"] = resp.headers["Location"]
                return result

            if "json" in resp.headers.get("Content-Type", ""):
                try:
                    return await resp.json(content_type=None)
                except ValueError:
                    return text

            return text

    async def executeSSE(self, url: str, headers: Dict = None, params: Dict = None):
        """
        Opens a Server-Sent Events (SSE) stream.

        :param url: Absolute URL or resource path (e.g. "/rest/events").
        :param headers: Optional; additional headers.
        :param params: Optional; query parameters (e.g. {"topics": "openhab/items/*/statechanged"}).

        :return: The open aiohttp.ClientResponse. Read it line by line with
                 ``async for line in response.content`` and close it with ``response.close()``.
        :raises aiohttp.ClientResponseError: If the server rejects the request.
        """
        session = await self._ensureSession()
        # identity: a compressed stream would be flushed late, events would arrive delayed
        requestHeaders = {"Accept": "text/event-stream", "Accept-Encoding": "identity", "Cache-Control": "no-cache"}
        requestHeaders.update({k: v for k, v in (headers or {}).items() if v is not None})

        resp = await session.get(self._buildUrl(url), headers=requestHeaders, params=self._cleanParams(params),
                                 timeout=aiohttp.ClientTimeout(total=None, sock_connect=self.SSE_CONNECT_TIMEOUT))
        try:
            await self._raiseForStatus(resp)
        except aiohttp.ClientResponseError:
            resp.release()
            raise
        return resp  # Caller must iterate resp.content

    #
    # PUBLIC WRAPPER METHODS
    #

    async def get(self, endpoint: str, headers: Dict = None, params: Dict = None):
        return await self.__executeRequest(headers, endpoint, "get", params=params)

    async def post(self, endpoint: str, headers: Dict = None, data=None, params: Dict = None):
        return await self.__executeRequest(headers, endpoint, "post", data=data, params=params)

    async def put(self, endpoint: str, headers: Dict = None, data=None, params: Dict = None):
        return await self.__executeRequest(headers, endpoint, "put", data=data, params=params)

    async def delete(self, endpoint: str, headers: Dict = None, data=None, params: Dict = None):
        return await self.__executeRequest(headers, endpoint, "delete", data=data, params=params)

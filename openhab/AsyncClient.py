import aiohttp
import asyncio
from typing import Optional, Dict, Any

class AsyncOpenHABClient:
    def __init__(
        self,
        url: str,
        username: str = None,
        password: str = None,
        token: str = None
    ):
        """
        Initializes the asynchronous OpenHAB client.
        """

        self.url = url.rstrip("/")
        self.username = username
        self.password = password
        self.token = token

        self.auth = None
        if username and password:
            self.auth = aiohttp.BasicAuth(username, password)

        self.session: Optional[aiohttp.ClientSession] = None
        self.isCloud = False
        self.isLoggedIn = False

    async def __aenter__(self):
        """
        Async context manager start (like "with ...").
        """

        headers = {}

        if self.token:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }

        self.session = aiohttp.ClientSession(
            auth=self.auth,
            headers=headers
        )

        await self.__login()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Async context manager end.
        """
        if self.session:
            await self.session.close()

    async def __login(self):
        """
        Asynchronous login / connectivity check.
        """

        if self.url == "https://myopenhab.org":
            self.isCloud = True
        else:
            self.isCloud = False

        try:
            async with self.session.get(self.url + "/rest", timeout=8) as resp:
                resp.raise_for_status()
                if resp.status == 200:
                    self.isLoggedIn = True

        except aiohttp.ClientResponseError as err:
            print(f"HTTP error occurred: {err}")
        except aiohttp.ClientConnectorError as err:
            print(f"Connection error occurred: {err}")
        except asyncio.TimeoutError as err:
            print(f"Timeout occurred: {err}")
        except Exception as err:
            print(f"Request exception occurred: {err}")

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
        """

        if not resourcePath or not method:
            raise ValueError("resourcePath and method must be specified!")

        method = method.lower()
        headers = headers or {}

        # Normalize
        if not resourcePath.startswith("/"):
            resourcePath = "/" + resourcePath

        if not resourcePath.startswith("/rest"):
            resourcePath = "/rest" + resourcePath

        url = self.url + resourcePath

        # Merge session headers + per-request headers
        request_headers = self.session.headers.copy()
        request_headers.update(headers)

        try:
            async with self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=request_headers,
                timeout=5
            ) as resp:

                location = resp.headers.get("Location")
                if location:
                    return resp

                resp.raise_for_status()

                text = await resp.text()

                if not text.strip():
                    return {"status": resp.status}

                content_type = resp.headers.get("Content-Type", "")

                if "application/json" in content_type:
                    return await resp.json()

                return text

        except aiohttp.ClientError as err:
            print(f"Request error: {err}")
            raise

    async def __executeSSE(self, url: str, headers: Dict = None):
        """
        Returns an async SSE stream iterator.
        """
        headers = headers or {}

        request_headers = self.session.headers.copy()
        request_headers.update(headers)

        resp = await self.session.get(url, headers=request_headers)

        resp.raise_for_status()

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

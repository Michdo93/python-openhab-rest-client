import requests


class StatusResponse(dict):
    """
    Marker for responses without a body (e.g. ``200 OK`` with an empty body,
    ``201 Created``, ``202 Accepted``).

    It is a plain ``dict`` with the keys ``status`` (HTTP status code) and,
    if the server sent one, ``location``. Because it is its own type, it can
    never be confused with a JSON response that happens to contain a
    ``status`` field (e.g. a thing status or a rule).
    """

    @property
    def status(self) -> int:
        return self["status"]


class OpenHABClient:
    DEFAULT_TIMEOUT = 10
    SSE_CONNECT_TIMEOUT = 10

    def __init__(self, url: str, username: str = None, password: str = None, token: str = None,
                 timeout: float = DEFAULT_TIMEOUT, verify=True):
        """
        Initializes the OpenHABClient instance.

        :param url: The base URL of the OpenHAB server (e.g., "http://127.0.0.1:8080").
        :param username: Optional; The username for Basic Authentication (default is None).
        :param password: Optional; The password for Basic Authentication (default is None).
        :param token: Optional; The Bearer Token for Token-based Authentication (default is None).
        :param timeout: Optional; Timeout in seconds for normal requests (default is 10).
        :param verify: Optional; TLS verification, passed on to requests (default is True).
        """
        self.url = url.rstrip("/")  # Remove trailing slash if present
        self.username = username
        self.password = password
        self.token = token
        self.timeout = timeout
        self.isCloud = False
        self.isLoggedIn = False
        self.auth = None

        self.session = requests.Session()
        self.session.verify = verify

        if self.token:
            # Use Token-based authentication
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        elif self.username and self.password:
            # Use Basic Authentication (also used by myopenHAB)
            self.auth = (self.username, self.password)
            self.session.auth = self.auth

        self.__login()

    def __login(self):
        """
        Checks whether the openHAB server is reachable and the credentials are accepted.

        If the server is "myopenhab.org", it sets the connection to the cloud service.
        """
        self.isCloud = self.url.rstrip("/") in ("https://myopenhab.org", "https://home.myopenhab.org")

        try:
            loginResponse = self.session.get(self.url + "/rest/", timeout=self.timeout)
            loginResponse.raise_for_status()
            self.isLoggedIn = loginResponse.ok
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP error occurred: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection error occurred: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout occurred: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request exception occurred: {err}")

    def _buildUrl(self, resourcePath: str) -> str:
        """Builds the absolute URL for a resource path (with or without the /rest prefix)."""
        if resourcePath.startswith("http://") or resourcePath.startswith("https://"):
            return resourcePath
        if not resourcePath.startswith("/"):
            resourcePath = "/" + resourcePath
        if not (resourcePath == "/rest" or resourcePath.startswith("/rest/") or resourcePath.startswith("/rest?")):
            resourcePath = f"/rest{resourcePath}"
        # "#" is valid inside openHAB UIDs (channel and action UIDs), but would start a URL fragment.
        path, sep, query = resourcePath.partition("?")
        resourcePath = path.replace("#", "%23") + sep + query
        return f"{self.url}{resourcePath}"

    @staticmethod
    def _cleanParams(params):
        """Removes parameters whose value is None and converts booleans to 'true'/'false'."""
        if not params:
            return None
        clean = {}
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, bool):
                value = str(value).lower()
            clean[key] = value
        return clean

    @staticmethod
    def _raiseForStatus(response):
        """
        Like response.raise_for_status(), but adds the error message that openHAB
        sends in the body ({"error": {"message": ..., "http-code": ...}}).
        """
        if response.status_code < 400:
            return
        message = ""
        try:
            body = response.json()
            if isinstance(body, dict):
                error = body.get("error")
                message = error.get("message", "") if isinstance(error, dict) else str(error or "")
        except ValueError:
            message = (response.text or "").strip()[:200]
        kind = "Client Error" if response.status_code < 500 else "Server Error"
        text = f"{response.status_code} {kind}: {response.reason} for url: {response.url}"
        if message:
            text += f" ({message})"
        raise requests.exceptions.HTTPError(text, response=response)

    def __executeRequest(self, headers: dict = None, resourcePath: str = None, method: str = None, data=None,
                         params=None):
        """
        Executes an HTTP request to the openHAB server.

        :param headers: Optional; A dictionary of headers to be sent with this request only.
        :param resourcePath: The path of the resource to interact with.
        :param method: The HTTP method (GET, POST, PUT, DELETE).
        :param data: Optional; The data to send in the request (for POST and PUT requests).
        :param params: Optional; Query parameters. None values are dropped.
        :return: The decoded JSON, the response text, or a StatusResponse for empty bodies.

        :raises ValueError: If the method is invalid or if the resource path is not provided.
        :raises requests.exceptions.HTTPError: For 4xx/5xx responses.
        """
        if not resourcePath or not method:
            raise ValueError('You must specify a valid resource path and HTTP method!')

        method = method.lower()
        if method not in ("get", "post", "put", "delete"):
            raise ValueError("Invalid HTTP method provided!")

        url = self._buildUrl(resourcePath)
        # Headers are only used for this request – the session headers stay untouched.
        headers = {k: v for k, v in (headers or {}).items() if v is not None}
        if isinstance(data, str):
            if data and not any(k.lower() == "content-type" for k in headers):
                # openHAB rejects bodies without a matching media type (415)
                isJson = data.lstrip()[:1] in ("{", "[")
                headers["Content-Type"] = "application/json" if isJson else "text/plain"
            data = data.encode("utf-8")

        response = self.session.request(method, url, data=data, params=self._cleanParams(params),
                                        headers=headers, timeout=self.timeout)

        # Pass on errors directly – the calling classes translate them.
        self._raiseForStatus(response)

        if "charset" not in response.headers.get("Content-Type", "").lower():
            response.encoding = "utf-8"  # openHAB sends UTF-8 (e.g. "21.5 °C") without declaring it

        if not response.content or not response.text.strip():
            result = StatusResponse(status=response.status_code)
            if response.headers.get("Location"):
                result["location"] = response.headers["Location"]
            return result

        if "json" in response.headers.get("Content-Type", ""):
            try:
                return response.json()
            except ValueError:
                return response.text

        return response.text  # Fallback: Return text response

    def executeSSE(self, url: str, headers: dict = None, params: dict = None):
        """
        Opens a Server-Sent Events (SSE) stream.

        The stream uses the session of this client, so token and Basic
        Authentication are sent as well. There is no read timeout, because an
        event stream may stay silent for a long time (openHAB sends an ALIVE
        message every few seconds).

        :param url: Absolute URL or resource path (e.g. "/rest/events?topics=openhab/items/*/statechanged").
        :param headers: Optional; additional headers.
        :param params: Optional; query parameters.

        :return: The streaming requests.Response object (iterate with iter_lines()).
        :raises requests.exceptions.HTTPError: If the server rejects the request.
        """
        # identity: a compressed stream would be flushed late, events would arrive delayed
        requestHeaders = {"Accept": "text/event-stream", "Accept-Encoding": "identity", "Cache-Control": "no-cache"}
        requestHeaders.update({k: v for k, v in (headers or {}).items() if v is not None})
        response = self.session.get(self._buildUrl(url), headers=requestHeaders, params=self._cleanParams(params),
                                    stream=True, timeout=(self.SSE_CONNECT_TIMEOUT, None))
        self._raiseForStatus(response)
        return response

    # Backwards compatibility: older versions called the name-mangled private method.
    _OpenHABClient__executeSSE = executeSSE

    def get(self, endpoint: str, headers: dict = None, params: dict = None):
        """
        Sends a GET request to the openHAB server.

        :param endpoint: The endpoint for the GET request (e.g., "/items").
        :param headers: Optional; Headers to be sent with the request.
        :param params: Optional; Query parameters for the GET request.

        :return: The response from the GET request, either as JSON or plain text.
        """
        return self.__executeRequest(headers, endpoint, "get", params=params)

    def post(self, endpoint: str, headers: dict = None, data=None, params: dict = None):
        """
        Sends a POST request to the openHAB server.

        :param endpoint: The endpoint for the POST request (e.g., "/items").
        :param headers: Optional; Headers to be sent with the request.
        :param data: Optional; The data to send in the POST request.
        :param params: Optional; Query parameters for the request.

        :return: The response from the POST request.
        """
        return self.__executeRequest(headers, endpoint, "post", data=data, params=params)

    def put(self, endpoint: str, headers: dict = None, data=None, params: dict = None):
        """
        Sends a PUT request to the openHAB server.

        :param endpoint: The endpoint for the PUT request (e.g., "/items").
        :param headers: Optional; Headers to be sent with the request.
        :param data: Optional; The data to send in the PUT request.
        :param params: Optional; Query parameters for the request.

        :return: The response from the PUT request.
        """
        return self.__executeRequest(headers, endpoint, "put", data=data, params=params)

    def delete(self, endpoint: str, headers: dict = None, data=None, params: dict = None):
        """
        Sends a DELETE request to the openHAB server.

        :param endpoint: The endpoint for the DELETE request (e.g., "/items").
        :param headers: Optional; Headers to be sent with the request.
        :param data: Optional; The data to send in the DELETE request.
        :param params: Optional; Query parameters for the request.

        :return: The response from the DELETE request.
        """
        return self.__executeRequest(headers, endpoint, "delete", data=data, params=params)

    def close(self):
        """Closes the underlying HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

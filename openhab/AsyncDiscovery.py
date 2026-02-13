from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncDiscovery:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncDiscovery class with an AsyncOpenHABClient instance.
        """
        self.client = client

    async def getDiscoveryBindings(self) -> list:
        """
        Gets all bindings that support discovery asynchronously.
        """
        headers = {"Accept": "application/json"}

        try:
            response = await self.client.get("/discovery", headers=headers)
            return response

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getBindingInfo(self, bindingID: str, language: str = None) -> dict:
        """
        Gets information about the discovery services for a binding asynchronously.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(
                f"/discovery/bindings/{bindingID}/info",
                headers=headers
            )
            return response

        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Discovery service not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def startBindingScan(self, bindingID: str, input: str = None) -> dict:
        """
        Starts asynchronous discovery process for a binding and returns the timeout in seconds.
        """
        headers = {"Accept": "text/plain"}
        params = {"input": input} if input else {}

        try:
            response = await self.client.post(
                f"/discovery/bindings/{bindingID}/scan",
                headers=headers,
                params=params
            )
            return response

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

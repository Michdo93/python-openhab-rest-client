from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncConfigDescriptions:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncConfigDescriptions class with an AsyncOpenHABClient instance.
        """
        self.client = client

    async def getConfigDescriptions(self, scheme: str = None, language: str = None) -> list:
        """
        Retrieves all available config descriptions asynchronously.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        params = {}
        if scheme:
            params["scheme"] = scheme

        try:
            response = await self.client.get(
                "/config-descriptions",
                headers=headers,
                params=params
            )
            return response

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getConfigDescription(self, uri: str, language: str = None) -> dict:
        """
        Retrieves a configuration description by URI asynchronously.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(
                f"/config-descriptions/{uri}",
                headers=headers
            )
            return response

        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Invalid URI syntax."}
            elif err.status == 404:
                return {"error": "Not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

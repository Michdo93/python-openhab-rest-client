from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncChannelTypes:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncChannelTypes class with an AsyncOpenHABClient instance.
        """
        self.client = client

    async def getChannelTypes(self, prefixes: str = None, language: str = None) -> list:
        """
        Retrieves all available channel types asynchronously.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        params = {}
        if prefixes:
            params["prefixes"] = prefixes

        try:
            response = await self.client.get(
                "/channel-types",
                headers=headers,
                params=params
            )

            # client.get() should already return JSON → no status wrapper necessary
            return response

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getChannelType(self, channelTypeUID: str, language: str = None) -> dict:
        """
        Retrieves a specific channel type asynchronously.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(
                f"/channel-types/{channelTypeUID}",
                headers=headers
            )
            return response

        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Channel type with provided channelTypeUID does not exist."}
            return {"error": f"HTTP error {err.status}: {err.message}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getLinkableItemTypes(self, channelTypeUID: str) -> list:
        """
        Retrieves the item types that can be linked to the specified trigger channel type asynchronously.
        """
        try:
            response = await self.client.get(
                f"/channel-types/{channelTypeUID}/linkableItemTypes",
                headers={"Accept": "application/json"}
            )
            return response

        except aiohttp.ClientResponseError as err:
            if err.status == 204:
                return {"error": "No content: channel type has no linkable items or is no trigger channel."}
            elif err.status == 404:
                return {"error": "Given channel type UID not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

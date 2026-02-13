from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncProfileTypes:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncProfileTypes class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getProfileTypes(self, channelTypeUID=None, itemType=None, language: str = None):
        """
        Gets all available profile types.

        :param channelTypeUID: Optional filter for the channel type.
        :param itemType: Optional filter for the item type.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of profile types or an error dictionary.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        params = {}
        if channelTypeUID:
            params["channelTypeUID"] = channelTypeUID
        if itemType:
            params["itemType"] = itemType

        try:
            response = await self.client.get("/profile-types", params=params, headers=headers)
            return response

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

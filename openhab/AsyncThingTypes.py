from .AsyncClient import AsyncOpenHABClient
import aiohttp

class AsyncThingTypes:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncThingTypes class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getThingTypes(self, bindingID: str = None, language: str = None):
        """
        Gets all available thing types without config description, channels, and properties.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        params = {"bindingId": bindingID} if bindingID else {}

        try:
            response = await self.client.get("/thing-types", headers=headers, params=params)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getThingType(self, thingTypeUID: str, language: str = None):
        """
        Gets a thing type by UID.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f"/thing-types/{thingTypeUID}", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "No Content."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

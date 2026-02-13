from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncModuleTypes:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncModuleTypes class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getModuleTypes(self, tags=None, typeFilter=None, language: str = None):
        """
        Get all available module types asynchronously.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        params = {}
        if tags:
            params["tags"] = tags
        if typeFilter:
            params["type"] = typeFilter

        try:
            response = await self.client.get("/module-types", headers=headers, params=params)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getModuleType(self, moduleTypeUID, language: str = None):
        """
        Get a single module type asynchronously.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f"/module-types/{moduleTypeUID}", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Module Type corresponding to the given UID not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

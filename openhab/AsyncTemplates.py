from .AsyncClient import AsyncOpenHABClient
import aiohttp

class AsyncTemplates:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncTemplates class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getTemplates(self, language: str = None) -> list:
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.get("/templates", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getTemplate(self, templateUID: str, language: str = None) -> dict:
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.get(f"/templates/{templateUID}", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Template corresponding to the given UID does not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

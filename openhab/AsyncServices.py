from .AsyncClient import AsyncOpenHABClient
import json
import aiohttp


class AsyncServices:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncServices class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getServices(self, language=None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/services", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getService(self, serviceID: str, language=None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f"/services/{serviceID}", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getServiceConfig(self, serviceID: str):
        try:
            response = await self.client.get(f"/services/{serviceID}/config", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 500:
                return {"error": "Configuration cannot be read due to internal error."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def updateServiceConfig(self, serviceID: str, configData: dict, language: str = None):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.put(f"/services/{serviceID}/config", data=json.dumps(configData), headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 500:
                return {"error": "Configuration cannot be updated due to internal error."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def deleteServiceConfig(self, serviceID: str):
        try:
            response = await self.client.delete(f"/services/{serviceID}/config",
                                                headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 500:
                return {"error": "Configuration cannot be updated due to internal error."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getServiceContexts(self, serviceID: str, language=None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f"/services/{serviceID}/contexts", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncPersistence:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncPersistence class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getServices(self, language: str = None) -> dict:
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.get("/persistence", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getServiceConfiguration(self, serviceID: str) -> dict:
        try:
            response = await self.client.get(f"/persistence/{serviceID}", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Service configuration not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def setServiceConfiguration(self, serviceID: str, config: dict) -> dict:
        config["serviceId"] = serviceID
        try:
            response = await self.client.put(
                f"/persistence/{serviceID}",
                data=config,
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Payload invalid."}
            elif err.status == 405:
                return {"error": "PersistenceServiceConfiguration not editable."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def deleteServiceConfiguration(self, serviceID: str) -> dict:
        try:
            response = await self.client.delete(f"/persistence/{serviceID}")
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Payload invalid."}
            elif err.status == 405:
                return {"error": "PersistenceServiceConfiguration not editable."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getItemsFromService(self, serviceID: str = None) -> dict:
        url = "/persistence/items"
        if serviceID:
            url += f"?serviceID={serviceID}"
        try:
            response = await self.client.get(url, headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getItemPersistenceData(self, itemName: str, serviceID: str, startTime: str = None, endTime: str = None, page: int = 1, pageLength: int = 50, boundary: bool = False, itemState: bool = False) -> dict:
        params = {
            "serviceID": serviceID,
            "starttime": startTime,
            "endtime": endTime,
            "page": page,
            "pagelength": pageLength,
            "boundary": boundary,
            "itemState": itemState
        }
        try:
            response = await self.client.get(f"/persistence/items/{itemName}", params=params, headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Unknown Item or persistence service."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def storeItemData(self, itemName: str, time: str, state: str, serviceID: str = None) -> dict:
        params = {"serviceID": serviceID, "time": time, "state": state}
        try:
            response = await self.client.put(f"/persistence/items/{itemName}", params=params)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Unknown Item or persistence service."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def deleteItemData(self, itemName: str, startTime: str, endTime: str, serviceID: str) -> dict:
        params = {"serviceID": serviceID, "starttime": startTime, "endtime": endTime}
        try:
            response = await self.client.delete(f"/persistence/items/{itemName}", params=params, headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Unknown persistence service."}
            elif err.status == 400:
                return {"error": "Invalid filter parameters."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

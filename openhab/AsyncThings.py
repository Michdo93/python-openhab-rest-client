from .AsyncClient import AsyncOpenHABClient
import json
import aiohttp
from typing import Optional

class AsyncThings:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncThings class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getThings(self, summary: bool = False, staticDataOnly: bool = False, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        params = {"summary": summary, "staticDataOnly": staticDataOnly}
        try:
            response = await self.client.get("/things", params=params, headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def createThing(self, thingData: dict, language: str = None):
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.post("/things", data=json.dumps(thingData), headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 409:
                return {"error": "A thing with the same uid already exists."}
            elif err.status == 400:
                return {"error": "A uid must be provided, if no binding can create a thing of this type."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getThing(self, thingUID: str, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.get(f"/things/{thingUID}", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def updateThing(self, thingUID: str, thingData: dict, language: str = None):
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.put(f"/things/{thingUID}", data=json.dumps(thingData), headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Thing not found."}
            elif err.status == 409:
                return {"error": "Thing could not be updated as it is not editable."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def deleteThing(self, thingUID: str, force: bool = False, language: str = None):
        headers = {"Accept-Language": language} if language else {}
        params = {"force": force}
        try:
            response = await self.client.delete(f"/things/{thingUID}", params=params, headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Thing not found."}
            elif err.status == 409:
                return {"error": "Thing could not be deleted because it's not editable."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def updateThingConfiguration(self, thingUID: str, configurationData: dict, language: str = None):
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.put(f"/things/{thingUID}/config", data=json.dumps(configurationData), headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Configuration of the thing is not valid."}
            elif err.status == 404:
                return {"error": "Thing not found."}
            elif err.status == 409:
                return {"error": "Thing could not be updated as it is not editable."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getThingConfigStatus(self, thingUID: str, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.get(f"/things/{thingUID}/config/status", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def setThingStatus(self, thingUID: str, enabled: bool, language: str = None):
        headers = {"Content-Type": "text/plain", "Accept": "*/*"}
        if language:
            headers["Accept-Language"] = language
        data = "true" if enabled else "false"
        try:
            response = await self.client.put(f"/things/{thingUID}/enable", data=data, headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Thing not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def enableThing(self, thingUID: str):
        return await self.setThingStatus(thingUID, True)

    async def disableThing(self, thingUID: str):
        return await self.setThingStatus(thingUID, False)

    async def updateThingFirmware(self, thingUID: str, firmwareVersion: str, language: Optional[str] = None):
        headers = {"Accept-Language": language} if language else {}

        try:
            response = await self.client.put(f'/things/{thingUID}/firmware/{firmwareVersion}', headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 400:
                return {"error": "Firmware update preconditions not satisfied."}
            elif status_code == 404:
                return {"error": "Thing not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Firmware update preconditions not satisfied."}
        elif status_code == 404:
            return {"error": "Thing not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getThingFirmwareStatus(self, thingUID: str, language: Optional[str] = None):
        headers = {"Accept": "*/*"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f'/things/{thingUID}/firmware/status', headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 204:
            return {"error": "No firmware status provided by this Thing."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getThingFirmwares(self, thingUID: str, language: Optional[str] = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f'/things/{thingUID}/firmwares', headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 204:
            return {"error": "No firmwares found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getThingStatus(self, thingUID: str, language: Optional[str] = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f'/things/{thingUID}/status', headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Thing not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Thing not found."}

        return {"error": f"Unexpected response: {status_code}"}

import json
import urllib.parse
import aiohttp
from .AsyncClient import AsyncOpenHABClient


class AsyncAddons:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncAddons class with an AsyncOpenHABClient instance.
        """
        self.client = client

    async def getAddons(self, serviceID: str = None, language: str = None) -> dict:
        params = {"serviceId": serviceID} if serviceID else {}
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/addons", headers=headers, params=params)

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 404:
                return {"error": "Service not found."}
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}
        elif status == 404:
            return {"error": "Service not found."}

        return {"error": f"Unexpected response: {status}"}

    async def getAddon(self, addonID: str, serviceID: str = None, language: str = None) -> dict:
        params = {"serviceId": serviceID} if serviceID else {}
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f"/addons/{addonID}", headers=headers, params=params)

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 404:
                return {"error": "Not found."}
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}
        elif status == 404:
            return {"error": "Not found."}

        return {"error": f"Unexpected response: {status}"}

    async def getAddonConfig(self, addonID: str, serviceID: str = None) -> dict:
        params = {"serviceId": serviceID} if serviceID else {}

        try:
            response = await self.client.get(
                f"/addons/{addonID}/config",
                headers={"Accept": "application/json"},
                params=params
            )

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 500:
                return {"error": "Configuration can not be read due to internal error."}
            elif status == 404:
                return {"error": "Add-on does not exist."}
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}
        elif status == 404:
            return {"error": "Add-on does not exist."}
        elif status == 500:
            return {"error": "Configuration can not be read due to internal error."}

        return {"error": f"Unexpected response: {status}"}

    async def updateAddonConfig(self, addonID: str, configData: dict, serviceID: str = None) -> dict:
        data = {**configData}
        if serviceID:
            data["serviceId"] = serviceID

        try:
            response = await self.client.put(
                f"/addons/{addonID}/config",
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                data=json.dumps(data)
            )

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 500:
                return {"error": "Configuration can not be updated due to internal error."}
            elif status == 404:
                return {"error": "Add-on does not exist."}
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}
        elif status == 404:
            return {"error": "Add-on does not exist."}
        elif status == 500:
            return {"error": "Configuration can not be updated due to internal error."}

        return {"error": f"Unexpected response: {status}"}

    async def installAddon(self, addonID: str, serviceID: str = None) -> dict:
        data = {"serviceId": serviceID} if serviceID else {}

        try:
            response = await self.client.post(f"/addons/{addonID}/install", data=data)

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 404:
                return {"error": "Not found."}
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}
        elif status == 404:
            return {"error": "Not found."}

        return {"error": f"Unexpected response: {status}"}

    async def uninstallAddon(self, addonID: str, serviceID: str = None) -> dict:
        data = {"serviceId": serviceID} if serviceID else {}

        try:
            response = await self.client.post(f"/addons/{addonID}/uninstall", data=data)

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 404:
                return {"error": "Not found."}
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}
        elif status == 404:
            return {"error": "Not found."}

        return {"error": f"Unexpected response: {status}"}

    async def getAddonServices(self, language: str = None) -> dict:
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/addons/services", headers=headers)

        except aiohttp.ClientResponseError as err:
            status = err.status
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status}"}

    async def getAddonSuggestions(self, language: str = None) -> dict:
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/addons/suggestions", headers=headers)

        except aiohttp.ClientResponseError as err:
            status = err.status
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status}"}

    async def getAddonTypes(self, serviceID: str = None, language: str = None) -> dict:
        params = {"serviceId": serviceID} if serviceID else {}
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/addons/types", headers=headers, params=params)

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 404:
                return {"error": "Service not found."}
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}
        elif status == 404:
            return {"error": "Service not found."}

        return {"error": f"Unexpected response: {status}"}

    async def installAddonFromUrl(self, url: str) -> dict:
        encoded = urllib.parse.quote(url, safe="")
        endpoint = f"/addons/url/{encoded}/install"

        try:
            response = await self.client.post(endpoint)

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 400:
                return {"error": "The given URL is malformed or not valid."}
            return {"error": f"HTTP error {status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}
        elif status == 400:
            return {"error": "The given URL is malformed or not valid."}

        return {"error": f"Unexpected response: {status}"}

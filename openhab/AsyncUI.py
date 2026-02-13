import json
import aiohttp
from .AsyncClient import AsyncOpenHABClient


class AsyncUI:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncUI class with an AsyncOpenHABClient.
        """
        self.client = client

    async def getUIComponents(self, namespace: str, summary: bool = False) -> list:
        params = {"summary": "true" if summary else "false"}
        headers = {"Accept": "application/json"}

        try:
            response = await self.client.get(f"/ui/components/{namespace}", headers=headers, params=params)

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}
        
        return {"error": f"Unexpected response: {status}"}

    async def addUIComponent(self, namespace: str, componentData: dict) -> dict:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = await self.client.post(
                f"/ui/components/{namespace}", 
                headers=headers, 
                data=json.dumps(componentData)
            )

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status}"}

    async def getUIComponent(self, namespace: str, componentUID: str) -> dict:
        headers = {"Accept": "application/json"}
        try:
            response = await self.client.get(f"/ui/components/{namespace}/{componentUID}", headers=headers)

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 404:
                return {"error": "Component not found."}
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
            return {"error": "Component not found."}

        return {"error": f"Unexpected response: {status}"}

    async def updateUIComponent(self, namespace: str, componentUID: str, componentData: dict) -> dict:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = await self.client.put(
                f"/ui/components/{namespace}/{componentUID}", 
                headers=headers, 
                data=json.dumps(componentData)
            )

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 404:
                return {"error": "Component not found."}
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
            return {"error": "Component not found."}

        return {"error": f"Unexpected response: {status}"}

    async def deleteUIComponent(self, namespace: str, componentUID: str) -> dict:
        try:
            response = await self.client.delete(f"/ui/components/{namespace}/{componentUID}")

        except aiohttp.ClientResponseError as err:
            status = err.status
            if status == 404:
                return {"error": "Component not found."}
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
            return {"error": "Component not found."}

        return {"error": f"Unexpected response: {status}"}

    async def getUITiles(self) -> list:
        headers = {"Accept": "application/json"}
        try:
            response = await self.client.get("/ui/tiles", headers=headers)

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status = response["status"]
        else:
            return response

        if status == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status}"}
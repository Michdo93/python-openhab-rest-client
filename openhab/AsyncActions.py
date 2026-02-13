import json
import aiohttp
from .AsyncClient import AsyncOpenHABClient


class AsyncActions:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncActions class with an AsyncOpenHABClient.
        """
        self.client = client

    async def getActions(self, thingUID: str, language: str = None) -> list:
        """
        Asynchronously get all available actions for provided thing UID.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f"/actions/{thingUID}", headers=headers)

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 204:
                return {"error": "No actions found."}
            elif status_code == 404:
                return {"error": f"Thing not found: {thingUID}"}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        # response is ok
        if isinstance(response, dict) and "status" in response:
            status_code = response["status"]
        else:
            return response

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 204:
            return {"error": "No actions found."}
        elif status_code == 404:
            return {"error": f"Thing not found: {thingUID}"}

        return {"error": f"Unexpected response: {status_code}"}

    async def executeAction(self, thingUID: str, actionUID: str, actionInputs: dict, language: str = None) -> str:
        """
        Asynchronously executes a thing action.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.post(
                f"/actions/{thingUID}/{actionUID}",
                headers=headers,
                data=json.dumps(actionInputs)
            )

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Action not found."}
            elif status_code == 500:
                return {"error": "Creation of action handler or execution failed."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status_code = response["status"]
        else:
            return response

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Action not found."}
        elif status_code == 500:
            return {"error": "Creation of action handler or execution failed."}

        return {"error": f"Unexpected response: {status_code}"}

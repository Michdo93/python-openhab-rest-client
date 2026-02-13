from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncInbox:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncInbox class with an AsyncOpenHABClient object.

        :param client: An instance of AsyncOpenHABClient used for REST-API communication.
        """
        self.client = client

    async def getDiscoveredThings(self, includeIgnored: bool = True):
        """
        Get all discovered things asynchronously.

        :param includeIgnored: Whether ignored entries should also be included (default: True).

        :return: A list of discovered things with details such as UID, flag, label, and properties.
        """
        try:
            response = await self.client.get(
                "/inbox",
                headers={"Accept": "application/json"},
                params={"includeIgnored": str(includeIgnored).lower()}
            )
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def removeDiscoveryResult(self, thingUID: str):
        """
        Removes the discovery result from the inbox asynchronously.

        :param thingUID: The UID of the discovered thing to be removed.

        :return: The API response to the delete request.
        """
        try:
            response = await self.client.delete(f"/inbox/{thingUID}")
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Discovery result not found in the inbox."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def approveDiscoveryResult(self, thingUID: str, thingLabel: str, newThingID: str = None, language: str = None):
        """
        Approves the discovery result by adding the thing to the registry asynchronously.

        :param thingUID: The UID of the discovered thing.
        :param thingLabel: The new name of the thing.
        :param newThingID: Optional new thing ID.
        :param language: Optional language preference.

        :return: The API response to the approval request.
        """
        headers = {"Content-Type": "text/plain"}
        if language:
            headers["Accept-Language"] = language

        params = {"newThingID": newThingID} if newThingID else {}

        try:
            response = await self.client.post(f"/inbox/{thingUID}/approve", headers=headers, params=params, data=thingLabel)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Invalid new thing ID."}
            elif err.status == 404:
                return {"error": "Thing unable to be approved."}
            elif err.status == 409:
                return {"error": "No binding found that supports this thing."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def ignoreDiscoveryResult(self, thingUID: str):
        """
        Flags a discovery result as ignored asynchronously.

        :param thingUID: The UID of the discovered thing.
        """
        try:
            response = await self.client.post(f"/inbox/{thingUID}/ignore")
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def unignoreDiscoveryResult(self, thingUID: str):
        """
        Removes the ignore flag from a discovery result asynchronously.

        :param thingUID: The UID of the discovered thing.
        """
        try:
            response = await self.client.post(f"/inbox/{thingUID}/unignore")
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

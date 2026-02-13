from .AsyncClient import AsyncOpenHABClient
import json
import aiohttp


class AsyncItems:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncItems class with an AsyncOpenHABClient object.

        :param client: An instance of AsyncOpenHABClient used for REST-API communication.
        """
        self.client = client

    async def getItems(self, type: str = None, tags: str = None, metadata: str = ".*",
                       recursive: bool = False, fields: str = None,
                       staticDataOnly: bool = False, language: str = None):
        """
        Get all available items asynchronously.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        params = {k: v for k, v in {
            "type": type,
            "tags": tags,
            "metadata": metadata,
            "recursive": str(recursive).lower(),
            "fields": fields,
            "staticDataOnly": str(staticDataOnly).lower(),
        }.items() if v is not None}

        try:
            response = await self.client.get("/items", headers=headers, params=params)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def addOrUpdateItems(self, items: list):
        """
        Adds or updates a list of items asynchronously.
        """
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        try:
            response = await self.client.put("/items", headers=headers, data=json.dumps(items))
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Payload is invalid."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getItem(self, itemName: str, metadata: str = ".*", recursive: bool = True, language: str = None):
        """
        Gets a single item asynchronously.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        params = {"metadata": metadata, "recursive": str(recursive).lower()}

        try:
            response = await self.client.get(f"/items/{itemName}", headers=headers, params=params)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def addOrUpdateItem(self, itemName: str, itemData: dict, language: str = None):
        """
        Adds or updates a single item asynchronously.
        """
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.put(f"/items/{itemName}", headers=headers, data=json.dumps(itemData))
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Payload invalid."}
            elif err.status == 404:
                return {"error": "Item not found or name in path invalid."}
            elif err.status == 405:
                return {"error": "Item not editable."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def sendCommand(self, itemName: str, command: str):
        """
        Sends a command to an item asynchronously.
        """
        headers = {"Content-Type": "text/plain"}
        try:
            response = await self.client.post(f"/items/{itemName}", headers=headers, data=command)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Item not found."}
            elif err.status == 400:
                return {"error": "Item command null."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def updateItemState(self, itemName: str, state: str, language: str = None):
        """
        Updates the state of an item asynchronously.
        """
        headers = {"Content-Type": "text/plain"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.put(f"/items/{itemName}/state", headers=headers, data=state)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Item state null."}
            elif err.status == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def deleteItem(self, itemName: str):
        """
        Removes an item asynchronously.
        """
        try:
            response = await self.client.delete(f"/items/{itemName}")
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Item not found or item not editable."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def addGroupMember(self, itemName: str, memberItemName: str):
        try:
            response = await self.client.put(f"/items/{itemName}/members/{memberItemName}")
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 405:
                return {"error": "Member item is not editable."}
            elif status_code == 404:
                return {"error": "Item or member item not found or item is not of type group item."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item or member item not found or item is not of type group item."}
        elif status_code == 405:
            return {"error": "Member item is not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    async def removeGroupMember(self, itemName: str, memberItemName: str):
        try:
            response = await self.client.delete(f"/items/{itemName}/members/{memberItemName}")
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 405:
                return {"error": "Member item is not editable."}
            elif status_code == 404:
                return {"error": "Item or member item not found or item is not of type group item."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item or member item not found or item is not of type group item."}
        elif status_code == 405:
            return {"error": "Member item is not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    async def addMetadata(self, itemName: str, namespace: str, metadata: dict):
        try:
            response = await self.client.put(
                f"/items/{itemName}/metadata/{namespace}",
                headers={"Content-Type": "application/json"},
                data=json.dumps(metadata)
            )
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 400:
                return {"error": "Metadata value empty."}
            elif status_code == 405:
                return {"error": "Metadata not editable."}
            elif status_code == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code in (200, 201):
            return {"message": "Created." if status_code == 201 else "OK"}
        elif status_code == 400:
            return {"error": "Metadata value empty."}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 405:
            return {"error": "Metadata not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    async def removeMetadata(self, itemName: str, namespace: str):
        try:
            response = await self.client.delete(f"/items/{itemName}/metadata/{namespace}")
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 405:
                return {"error": "Meta data not editable."}
            elif status_code == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 405:
            return {"error": "Meta data not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getMetadataNamespaces(self, itemName: str, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.get(f"/items/{itemName}/metadata/namespaces", headers=headers)
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getSemanticItem(self, itemName: str, semanticClass: str, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.get(f"/items/{itemName}/semantic/{semanticClass}", headers=headers)
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getItemState(self, itemName: str):
        headers = {"Accept": "text/plain"}
        try:
            response = await self.client.get(f"/items/{itemName}/state", headers=headers)
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def updateItemState(self, itemName: str, state: str, language: str = None):
        headers = {"Content-Type": "text/plain"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.put(f"/items/{itemName}/state", headers=headers, data=state)
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 400:
                return {"error": "Item state null."}
            elif status_code == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 202:
            return {"message": "Accepted."}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 400:
            return {"error": "Item state null."}

        return {"error": f"Unexpected response: {status_code}"}

    async def addTag(self, itemName: str, tag: str):
        try:
            response = await self.client.put(f"/items/{itemName}/tags/{tag}")
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 405:
                return {"error": "Item not editable."}
            elif status_code == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 405:
            return {"error": "Item not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    async def removeTag(self, itemName: str, tag: str):
        try:
            response = await self.client.delete(f"/items/{itemName}/tags/{tag}")
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 405:
                return {"error": "Item not editable."}
            elif status_code == 404:
                return {"error": "Item not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Item not found."}
        elif status_code == 405:
            return {"error": "Item not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    async def purgeOrphanedMetadata(self):
        try:
            response = await self.client.post("/items/metadata/purge")
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}
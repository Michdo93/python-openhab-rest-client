from .client import OpenHABClient
import json

class Items:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Items class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllItems(
        self,
        language: str = None,
        type: str = None,
        tags: str = None,
        metadata: str = ".*",
        recursive: bool = False,
        fields: str = None,
        staticDataOnly: bool = False,
    ):
        """
        Get all available items.

        :param language: Optional; Language filter for header "Accept-Language".
        :param type: Optional; Item type filter.
        :param tags: Optional; Item tag filter.
        :param metadata: Optional; Metadata selector (default: .*).
        :param recursive: Optional; Whether to fetch group members recursively (default: False).
        :param fields: Optional; Limit to specific fields (comma-separated).
        :param staticDataOnly: Optional; Only returns cached data (default: False).

        :return: A dictionary or list containing the item data as returned by the API.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {
            "type": type,
            "tags": tags,
            "metadata": metadata,
            "recursive": str(recursive).lower(),
            "fields": fields,
            "staticDataOnly": str(staticDataOnly).lower(),
        }

        # Remove None values from parameters
        params = {key: value for key, value in params.items() if value is not None}

        return self.client.get("/items", header=header, params=params)

    def addOrUpdateItems(self, items: list):
        """
        Adds a list of items to the registry or updates the existing items.

        :param items: A list of item data (Dictionary).

        :return: A response object or confirmation that the items were successfully added or updated.
        """
        return self.client.put("/items", data=json.dumps(items), header={"Content-Type": "application/json"})

    def getItem(self, itemName: str, language: str = None, metadata: str = ".*", recursive: bool = True):
        """
        Gets a single item.

        :param itemName: The name of the item.
        :param language: Optional; Language filter for header "Accept-Language".
        :param metadata: Optional; Metadata selector (default: .*).
        :param recursive: Optional; Whether to fetch group members recursively (default: True).

        :return: A dictionary containing the requested item data.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {
            "metadata": metadata,
            "recursive": str(recursive).lower(),
        }

        return self.client.get(f"/items/{itemName}", header=header, params=params)

    def addOrUpdateItem(self, itemName: str, itemData: dict, language: str = None):
        """
        Adds a new item to the registry or updates the existing item.

        :param itemName: The name of the item.
        :param itemData: The data of the item (Dictionary).
        :param language: Optional; Language filter for header "Accept-Language".

        :return: A response object or confirmation that the item was successfully added or updated.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language
        
        return self.client.put(f"/items/{itemName}", header=header, data=json.dumps(itemData))

    def sendCommand(self, itemName: str, command: str):
        """
        Sends a command to an item.

        :param itemName: The name of the item.
        :param command: The command to be sent (e.g., ON, OFF).

        :return: A response object or confirmation that the command was successfully sent.
        """
        return self.client.post(f"/items/{itemName}", header={"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}, data=command)

    def postUpdate(self, itemName: str, state: str):
        """
        Updates the state of an item.

        :param itemName: The name of the item.
        :param state: The state to be signaled for the item.

        :return: A response object or confirmation that the state was successfully updated.
        """
        return self.updateItemState(itemName, state)

    def deleteItem(self, itemName: str):
        """
        Removes an item from the registry.

        :param itemName: The name of the item.

        :return: A response object or confirmation that the item was successfully deleted.
        """
        return self.client.delete(f"/items/{itemName}")

    def addGroupMember(self, itemName: str, memberItemName: str):
        """
        Adds a new member to a group item.

        :param itemName: The name of the group item.
        :param memberItemName: The name of the member item.

        :return: A response object or confirmation that the group member was successfully added.
        """
        return self.client.put(f"/items/{itemName}/members/{memberItemName}")

    def removeGroupMember(self, itemName: str, memberItemName: str):
        """
        Removes an existing member from a group item.

        :param itemName: The name of the group item.
        :param memberItemName: The name of the member item.

        :return: A response object or confirmation that the group member was successfully removed.
        """
        return self.client.delete(f"/items/{itemName}/members/{memberItemName}")

    def addMetadata(self, itemName: str, namespace: str, metadata: dict):
        """
        Adds metadata to an item.

        :param itemName: The name of the item.
        :param namespace: The namespace of the metadata.
        :param metadata: A dictionary containing the metadata.

        :return: A response object or confirmation that the metadata was successfully added.
        """
        return self.client.put(f"/items/{itemName}/metadata/{namespace}", header={"Content-Type": "application/json"}, data=json.dumps(metadata))

    def removeMetadata(self, itemName: str, namespace: str):
        """
        Removes metadata from an item.

        :param itemName: The name of the item.
        :param namespace: The namespace of the metadata.

        :return: A response object or confirmation that the metadata was successfully removed.
        """
        return self.client.delete(f"/items/{itemName}/metadata/{namespace}")

    def getMetadataNamespaces(self, itemName: str, language: str = None):
        """
        Gets the namespaces of an item.

        :param itemName: The name of the item.
        :param language: Optional; Language filter for header "Accept-Language".

        :return: A list of namespaces associated with the item.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/items/{itemName}/metadata/namespaces", header=header)

    def getSemanticItem(self, itemName: str, semanticClass: str, language: str = None):
        """
        Gets the item that defines the requested semantics of an item.

        :param itemName: The name of the item.
        :param semanticClass: The requested semantic class.
        :param language: Optional; Language filter for header "Accept-Language".

        :return: A dictionary containing the semantic item data.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/items/{itemName}/semantic/{semanticClass}", header=header)

    def getItemState(self, itemName: str):
        """
        Gets the state of an item.

        :param itemName: The name of the item.

        :return: A dictionary containing the current state of the item.
        """
        return self.client.get(f"/items/{itemName}/state")

    def updateItemState(self, itemName: str, state: str, language: str = None):
        """
        Updates the state of an item.

        :param itemName: The name of the item.
        :param state: The new state of the item.
        :param language: Optional; Language filter for header "Accept-Language".

        :return: A response object or confirmation that the state was successfully updated.
        """
        header = {"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}
        if language:
            header["Accept-Language"] = language

        return self.client.put(f"/items/{itemName}/state", header=header, data=state)
            
    def addTag(self, itemName: str, tag: str):
        """
        Adds a tag to an item.

        :param itemName: The name of the item.
        :param tag: The tag to be added.

        :return: A response object or confirmation that the tag was successfully added.
        """
        return self.client.put(f"/items/{itemName}/tags/{tag}")

    def removeTag(self, itemName: str, tag: str):
        """
        Removes a tag from an item.

        :param itemName: The name of the item.
        :param tag: The tag to be removed.

        :return: A response object or confirmation that the tag was successfully removed.
        """
        return self.client.delete(f"/items/{itemName}/tags/{tag}")

    def purgeOrphanedMetadata(self):
        """
        Remove unused/orphaned metadata.

        :return: A response object or confirmation that orphaned metadata was successfully purged.
        """
        return self.client.post("/items/metadata/purge")

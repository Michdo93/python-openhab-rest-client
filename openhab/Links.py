from .client import OpenHABClient
import json
from urllib.parse import quote

class Links:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Links class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllLinks(self, channelUID: str = None, itemName: str = None) -> list:
        """
        Gets all available links.

        :param channelUID: Optional; Filters by the Channel UID.
        :param itemName: Optional; Filters by the Item Name.

        :return: A list of links containing details such as ItemName, ChannelUID, and configuration.
        """
        params = {}
        if channelUID:
            params["channelUID"] = channelUID
        if itemName:
            params["itemName"] = itemName
        
        return self.client.get("/links", params=params, header={"Content-Type": "application/json"})

    def getIndividualLink(self, itemName: str, channelUID: str) -> dict:
        """
        Retrieves an individual link.

        :param itemName: The name of the item.
        :param channelUID: The UID of the channel.

        :return: The link with details of the item, channel UID, and configuration.
        """
        itemName = quote(itemName, safe="")
        channelUID = quote(channelUID, safe="")
        
        return self.client.get(f"/links/{itemName}/{channelUID}", header={"Accept": "application/json"})

    def linkItemToChannel(self, itemName: str, channelUID: str, configuration: dict) -> dict:
        """
        Links an item to a channel.

        :param itemName: The name of the item.
        :param channelUID: The UID of the channel.
        :param configuration: The configuration for the link.

        :return: The API response when the link is successfully created.
        """
        itemName = quote(itemName, safe="")
        channelUID = quote(channelUID, safe="")
        
        return self.client.put(f"/links/{itemName}/{channelUID}", data=json.dumps({"itemName": itemName, "channelUID": channelUID, "configuration": configuration}), header={"Content-Type": "application/json"})

    def unlinkItemFromChannel(self, itemName: str, channelUID: str) -> dict:
        """
        Unlinks an item from a channel.

        :param itemName: The name of the item.
        :param channelUID: The UID of the channel.

        :return: The API response when the link is successfully removed.
        """
        itemName = quote(itemName, safe="")
        channelUID = quote(channelUID, safe="")
        
        return self.client.delete(f"/links/{itemName}/{channelUID}", header={"Content-Type": "application/json"})

    def deleteAllLinks(self, object: str) -> dict:
        """
        Delete all links that refer to an item or thing.

        :param object: The name of the item or the UID of the thing.

        :return: The API response when all links are successfully deleted.
        """
        return self.client.delete(f"/links/{object}")

    def getOrphanLinks(self) -> list:
        """
        Get orphan links between items and broken/non-existent thing channels.

        :return: A list of orphan links.
        """
        return self.client.get("/links/orphans", header={"Accept": "application/json"})

    def purgeUnusedLinks(self) -> dict:
        """
        Remove unused/orphaned links.

        :return: The API response when the links are successfully removed.
        """        
        return self.client.post("/links/purge")

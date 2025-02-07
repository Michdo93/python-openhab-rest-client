from .Client import OpenHABClient
import json

class Inbox:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Inbox class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllDiscoveredThings(self, includeIgnored: bool = True) -> list:
        """
        Get all discovered things.

        :param includeIgnored: Whether ignored entries should also be included (default: True).
        
        :return: A list of discovered things with details such as UID, flag, label, and properties.
        """        
        return self.client.get("/inbox", params={"includeIgnored": str(includeIgnored).lower()})

    def removeDiscoveryResult(self, thingUID: str) -> dict:
        """
        Removes the discovery result from the inbox.

        :param thingUID: The UID of the discovered thing to be removed.

        :return: The API response to the delete request.
        """        
        return self.client.delete(f"/inbox/{thingUID}")

    def approveDiscoveryResult(self, thingUID: str, thingLabel: str, newThingID: str = None, language: str = None) -> dict:
        """
        Approves the discovery result by adding the thing to the registry.
        
        :param thingUID: The UID of the discovered thing.
        :param thingLabel: The new name of the thing.
        :param newThingID: Optional: The new thing ID.
        :param language: Optional: Language preference for the response.

        :return: The API response to the approval request.
        """
        return self.client.post(f"/inbox/{thingUID}/approve", header={"Accept-Language": language, "Content-Type": "text/plain"} if language else {"Content-Type": "text/plain"}, params={"newThingID": newThingID} if newThingID else {}, data=thingLabel)

    def ignoreDiscoveryResult(self, thingUID: str) -> dict:
        """
        Flags a discovery result as ignored for further processing.

        :param thingUID: The UID of the discovered thing.

        :return: The API response to the ignore request.
        """
        return self.client.post(f"/inbox/{thingUID}/ignore")

    def unignoreDiscoveryResult(self, thingUID: str) -> dict:
        """
        Removes the ignore flag from a discovery result.

        :param thingUID: The UID of the discovered thing.

        :return: The API response to the unignore request.
        """
        return self.client.post(f"/inbox/{thingUID}/unignore")

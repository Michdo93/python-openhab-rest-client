from .Client import OpenHABClient
import json

class Actions:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Actions class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllActions(self, thingUID: str, language: str = None) -> list:
        """
        Get all available actions for provided thing UID.

        :param thingUID: The UID of the thing for which actions are to be retrieved.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of actions.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/actions/{thingUID}", header=header)

    def executeAction(self, thingUID: str, actionUID: str, actionInputs: dict, language: str = None) -> str:
        """
        Executes a thing action.

        :param thingUID: The UID of the thing on which the action is to be executed.
        :param actionUID: The UID of the action to be executed.
        :param actionInputs: The inputs for the action as a dictionary.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A response from the server.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.post(f"/actions/{thingUID}/{actionUID}", header=header, data=json.dumps(actionInputs))

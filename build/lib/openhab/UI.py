from .Client import OpenHABClient
import json

class UI:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the UI class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getUiComponents(self, namespace: str, summary: bool = False):
        """
        Get all registered UI components in the specified namespace.

        :param namespace: The namespace for which UI components should be retrieved.
        :param summary: If True, only summary fields will be returned.

        :return: A list of UI components (JSON).
        """
        return self.client.get(f"/ui/components/{namespace}", params={'summary': summary} if summary else {})

    def addUiComponent(self, namespace: str, componentData):
        """
        Add a UI component in the specified namespace.

        :param namespace: The namespace where the UI component should be added.
        :param componentData: The data of the UI component (JSON) to be added.

        :return: The response to the request (JSON).
        """
        return self.client.post(f"/ui/components/{namespace}", data=json.dumps(componentData), header={"Content-Type": "application/json"})

    def getUiComponent(self, namespace: str, componentUID: str):
        """
        Get a specific UI component in the specified namespace.

        :param namespace: The namespace where the UI component is located.
        :param componentUID: The UID of the UI component to retrieve.

        :return: The UI component (JSON).
        """
        return self.client.get(f"/ui/components/{namespace}/{componentUID}")

    def updateUiComponent(self, namespace: str, componentUID: str, componentData):
        """
        Update a specific UI component in the specified namespace.

        :param namespace: The namespace where the UI component should be updated.
        :param componentUID: The UID of the UI component to update.
        :param componentData: The new data for the UI component (JSON).

        :return: The response to the request (JSON).
        """
        return self.client.put(f"/ui/components/{namespace}/{componentUID}", data=json.dumps(componentData))

    def deleteUiComponent(self, namespace: str, componentUID: str):
        """
        Remove a specific UI component in the specified namespace.

        :param namespace: The namespace where the UI component should be removed.
        :param componentUID: The UID of the UI component to delete.

        :return: The response to the request (JSON).
        """
        return self.client.delete(f"/ui/components/{namespace}/{componentUID}")

    def getUiTiles(self):
        """
        Get all registered UI tiles.

        :return: A list of UI tiles (JSON).
        """
        return self.client.get("/ui/tiles")

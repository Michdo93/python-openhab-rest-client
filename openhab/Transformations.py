from .client import OpenHABClient
import json

class Transformations:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Transformations class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getTransformations(self):
        """
        Get a list of all transformations.

        :return: A list of transformations (JSON).
        """
        return self.client.get("/transformations")

    def getTransformation(self, transformationUID: str):
        """
        Get a single transformation.

        :param transformationUID: The transformationUID of the transformation to retrieve.

        :return: The transformation (JSON).
        """
        return self.client.get(f"/transformations/{transformationUID}")

    def updateTransformation(self, transformationUID: str, transformationData):
        """
        Update a single transformation.

        :param transformationUID: The transformationUID of the transformation to update.
        :param transformationData: The new data for the transformation.

        :return: The response to the transformation update request (JSON).
        """
        return self.client.put(f"/transformations/{transformationUID}", data=json.dumps(transformationData), header={"Content-Type": "application/json"})

    def deleteTransformation(self, transformationUID: str):
        """
        Delete a single transformation.

        :param transformationUID: The transformationUID of the transformation to delete.

        :return: The response to the transformation delete request (JSON).
        """
        return self.client.delete(f"/transformations/{transformationUID}")

    def getTransformationServices(self):
        """
        Get all transformation services.

        :return: A list of transformation services (JSON).
        """
        return self.client.get("/transformations/services")

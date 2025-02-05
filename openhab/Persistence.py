from .client import OpenHABClient
import json

class Persistence:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Persistence class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllServices(self) -> dict:
        """
        Gets a list of persistence services.

        :return: A list of persistence services with IDs, labels, and types.
        """        
        return self.client.get("/persistence")

    def getServiceConfiguration(self, serviceId: str) -> dict:
        """
        Gets a persistence service configuration.

        :param serviceId: The ID of the persistence service.

        :return: The configuration of the service.
        """        
        return self.client.get(f"/persistence/{serviceId}")

    def setServiceConfiguration(self, serviceId: str, config: dict) -> dict:
        """
        Sets a persistence service configuration.

        :param serviceId: The ID of the persistence service.
        :param config: The configuration data.

        :return: The response from the API after modification.
        """        
        return self.client.put(f"/persistence/{serviceId}", data=json.dumps({'serviceId': serviceId}), header={"Content-Type": "application/json", "Accept": "application/json"})

    def deleteServiceConfiguration(self, serviceId: str) -> dict:
        """
        Deletes a persistence service configuration.

        :param serviceId: The ID of the persistence service.

        :return: The response from the API after deleting the configuration.
        """
        return self.client.delete(f"/persistence/{serviceId}")

    def getItemsForService(self, serviceId: str) -> dict:
        """
        Gets a list of items available via a specific persistence service.

        :param serviceId: The ID of the persistence service.

        :return: A list of items with their last and earliest timestamps.
        """
        
        return self.client.get(f"/persistence/items?serviceId={serviceId}")

    def getItemPersistenceData(self, serviceId: str, itemName: str, startTime: str = None, endTime: str = None, page: int = 1, pageLength: int = 50) -> dict:
        """
        Gets item persistence data from the persistence service.

        :param serviceId: The ID of the persistence service.
        :param itemName: The name of the item.
        :param startTime: The start time for the data. Defaults to 1 day before `endTime`.
        :param endTime: The end time for the data. Defaults to the current time.
        :param page: The page of data. Defaults to `1`.
        :param pageLength: The number of data points per page. Defaults to `50`.

        :return: The retrieved data points of the item.
        """
        return self.client.get(f"/persistence/items/{itemName}", params={"serviceId": serviceId, "starttime": startTime, "endtime": endTime, "page": page, "pagelength": pageLength})

    def storeItemData(self, serviceId: str, itemName: str, time: str, state: str) -> dict:
        """
        Stores item persistence data into the persistence service.

        :param serviceId: The ID of the persistence service.
        :param itemName: The name of the item.
        :param time: The time of the storage.
        :param state: The state of the item to be stored.

        :return: The response from the API after storing the data.
        """
        return self.client.put(f"/persistence/items/{itemName}", params={"serviceId": serviceId, "time": time, "state": state})

    def deleteItemData(self, serviceId: str, itemName: str, startTime: str, endTime: str) -> dict:
        """
        Deletes item persistence data from a specific persistence service in a given time range.

        :param serviceId: The ID of the persistence service.
        :param itemName: The name of the item.
        :param startTime: The start time of the data to be deleted.
        :param endTime: The end time of the data to be deleted.

        :return: The response from the API after deleting the data.
        """

        return self.client.delete(f"/persistence/items/{itemName}", params={"serviceId": serviceId, "starttime": startTime, "endtime": endTime})

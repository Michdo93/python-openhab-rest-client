from .Client import OpenHABClient, StatusResponse
import json
import requests


class Persistence:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Persistence class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getServices(self, language: str = None) -> dict:
        """
        Gets a list of persistence services.

        :return: A list of persistence services with IDs, labels, and types.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = self.client.get("/persistence", headers=headers)

            if isinstance(response, StatusResponse):
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def getServiceConfiguration(self, serviceID: str) -> dict:
        """
        Gets a persistence service configuration.

        :param serviceID: The ID of the persistence service.

        :return: The configuration of the service.
        """
        try:
            response = self.client.get(f"/persistence/{serviceID}", headers={"Accept": "application/json"})

            if isinstance(response, StatusResponse):
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Service configuration not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Service configuration not found."}

        return {"error": f"Unexpected response: {status_code}"}

    def setServiceConfiguration(self, serviceID: str, config: dict) -> dict:
        """
        Sets a persistence service configuration.

        :param serviceID: The ID of the persistence service.
        :param config: The configuration data.

        :return: The response from the API after modification.
        """
        try:
            config["serviceId"] = serviceID  

            response = self.client.put(
                f"/persistence/{serviceID}",
                data=json.dumps(config),
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )

            if isinstance(response, StatusResponse):
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Payload invalid."}
            elif status_code == 405:
                return {"error": "PersistenceServiceConfiguration not editable."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 201:
            return {"message": "PersistenceServiceConfiguration created."}
        elif status_code == 400:
            return {"error": "Payload invalid."}
        elif status_code == 405:
            return {"error": "PersistenceServiceConfiguration not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteServiceConfiguration(self, serviceID: str) -> dict:
        """
        Deletes a persistence service configuration.

        :param serviceID: The ID of the persistence service.

        :return: The response from the API after deleting the configuration.
        """
        try:
            response = self.client.delete(f"/persistence/{serviceID}")

            if isinstance(response, StatusResponse):
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                return {"error": "Payload invalid."}
            elif status_code == 405:
                return {"error": "PersistenceServiceConfiguration not editable."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Payload invalid."}
        elif status_code == 405:
            return {"error": "PersistenceServiceConfiguration not editable."}

        return {"error": f"Unexpected response: {status_code}"}

    def getItemsFromService(self, serviceID: str = None, itemName: str = None) -> dict:
        """
        Gets a list of items available via a specific persistence service.

        :param serviceID: Optional; The ID of the persistence service (default service if omitted).
        :param itemName: Optional; Only return information for this item.

        :return: A list of items with their last and earliest timestamps.
        """
        try:
            response = self.client.get("/persistence/items", headers={"Accept": "application/json"},
                                       params={"serviceId": serviceID, "itemName": itemName})

            if isinstance(response, StatusResponse):
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Unknown persistence service."}
            if status_code == 405:
                return {"error": "The persistence service does not provide item information."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def getItemPersistenceData(self, itemName: str, serviceID: str = None, startTime: str = None, endTime: str = None,
                               page: int = None, pageLength: int = None, boundary: bool = False,
                               itemState: bool = False, displayState: bool = None, language: str = None) -> dict:
        """
        Gets item persistence data from the persistence service.

        :param itemName: The name of the item.
        :param serviceID: Optional; The ID of the persistence service. If omitted, the default service is used.
        :param startTime: Optional; Start time (ISO 8601, e.g. "2026-10-30T00:00:00.000Z"). Defaults to 1 day before `endTime`.
        :param endTime: Optional; End time (ISO 8601). Defaults to the current time.
        :param page: Optional; Page number, starting at 0. Paging is only active if `pageLength` is set as well.
        :param pageLength: Optional; Number of data points per page. Without it, all data points are returned.
        :param boundary: Optional; Also return the values just before and after the time range (default: False).
        :param itemState: Optional; Add the current item state at the end of the series (default: False).
        :param displayState: Optional; Add a formatted display state to every data point (openHAB 5.0+).
        :param language: Optional; Value for the "Accept-Language" header.

        :return: The retrieved data points of the item.
        """
        if pageLength is not None and page is None:
            page = 0
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = self.client.get(f"/persistence/items/{itemName}", params={
                                       "serviceId": serviceID, "starttime": startTime, "endtime": endTime, "page": page, "pagelength": pageLength, "boundary": boundary, "itemState": itemState,
                                       "displayState": displayState}, headers=headers)

            if isinstance(response, StatusResponse):
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Unknown Item or persistence service."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Unknown Item or persistence service."}

        return {"error": f"Unexpected response: {status_code}"}

    def storeItemData(self, itemName: str, time: str, state: str, serviceID: str = None) -> dict:
        """
        Stores item persistence data into the persistence service.

        :param serviceID: The ID of the persistence service.
        :param itemName: The name of the item.
        :param time: The time of the storage.
        :param state: The state of the item to be stored.

        :return: The response from the API after storing the data.
        """
        try:
            response = self.client.put(f"/persistence/items/{itemName}", params={
                                       "serviceId": serviceID, "time": time, "state": state})

            if isinstance(response, StatusResponse):
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Unknown Item or persistence service."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Unknown Item or persistence service."}

        return {"error": f"Unexpected response: {status_code}"}

    def deleteItemData(self, itemName: str, startTime: str, endTime: str, serviceID: str) -> dict:
        """
        Deletes item persistence data from a specific persistence service in a given time range.

        :param serviceID: The ID of the persistence service.
        :param itemName: The name of the item.
        :param startTime: The start time of the data to be deleted.
        :param endTime: The end time of the data to be deleted.

        :return: The response from the API after deleting the data.
        """
        try:
            response = self.client.delete(f"/persistence/items/{itemName}", params={
                                          "serviceId": serviceID, "starttime": startTime, "endtime": endTime}, headers={"Accept": "application/json"})

            if isinstance(response, StatusResponse):
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 400:
                # openHAB uses 400 for invalid filters and for read-only services (e.g. rrd4j)
                return {"error": f"Invalid filter parameters or service not modifiable: {str(err)}"}
            elif status_code == 404:
                return {"error": "Unknown persistence service."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Unknown persistence service."}
        elif status_code == 400:
            return {"error": "Invalid filter parameters."}

        return {"error": f"Unexpected response: {status_code}"}

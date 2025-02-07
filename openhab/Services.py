from .Client import OpenHABClient
import json

class Services:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Services class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getServices(self, language=None):
        """
        Get all configurable services.

        :param language: Optional language setting (as header).

        :return: A list of services (JSON).
        """
        return self.client.get("/services", header={"Accept-Language": language} if language else {})

    def getService(self, serviceID: str, language=None):
        """
        Get configurable service for the given service ID.

        :param serviceID: The ID of the service to retrieve.
        :param language: Optional language setting (as header).

        :return: The service object (JSON).
        """
        return self.client.get(f"/services/{serviceID}", header={"Accept-Language": language} if language else {})

    def getServiceConfig(self, serviceID: str):
        """
        Get service configuration for the given service ID.

        :param serviceID: The ID of the service.

        :return: The configuration of the service (JSON).
        """
        return self.client.get(f"/services/{serviceID}/config")

    def updateServiceConfig(self, serviceID: str, configData: dict):
        """
        Updates a service configuration for the given service ID and returns the old configuration.

        :param serviceID: The ID of the service.
        :param configData: The new configuration data (as a dictionary).

        :return: The old configuration of the service (JSON).
        """
        return self.client.put(f"/services/{serviceID}/config", data=json.dumps(configData), header={"Content-type": "application/json", "Accept": "application/json"})

    def deleteServiceConfig(self, serviceID: str):
        """
        Deletes a service configuration for the given service ID and returns the old configuration.

        :param serviceID: The ID of the service.

        :return: The old configuration of the service (JSON).
        """
        return self.client.delete(f"/services/{serviceID}/config", header={"Accept": "application/json"})

    def getServiceContexts(self, serviceID: str, language=None):
        """
        Get existing multiple context service configurations for the given factory PID.

        :param serviceID: The ID of the service.
        :param language: Optional language setting (as header).

        :return: A list of contexts (JSON).
        """
        header = {"Accept": "application/json"}  # Default to application/json
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/services/{serviceID}/contexts", header=header)

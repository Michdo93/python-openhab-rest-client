from .Client import OpenHABClient

class Discovery:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Discovery class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllDiscoveryBindings(self) -> list:
        """
        Gets all bindings that support discovery.

        :return: Eine Liste der Bindings als Strings.
        """
        return self.client.get("/discovery")

    def startBindingScan(self, bindingID: str) -> int:
        """
        Starts asynchronous discovery process for a binding and returns the timeout in seconds of the discovery operation.

        :param bindingID: The ID of the binding for which the discovery is to be started.

        :return: Timeout duration of the discovery operation in seconds.
        """        
        return self.client.post(f"/discovery/bindings/{bindingID}/scan")

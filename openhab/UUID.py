from .Client import OpenHABClient

class UUID:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the UUID class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getUUID(self) -> str:
        """
        A unified unique id.

        :return: The UUID as String.
        """
        return self.client.get("/uuid").strip()
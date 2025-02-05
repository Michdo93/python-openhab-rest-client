from .client import OpenHABClient

class Systeminfo:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Systeminfo class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getSystemInfo(self, language: str = None):
        """
        Gets information about the system.

        :return: A Dictionary with system informations.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get("/systeminfo", header=header)

    def getUomInfo(self, language: str = None):
        """
        Get all supported dimensions and their system units.

        :return: A Dictionary with UOM informations.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get("/systeminfo/uom", header=header)

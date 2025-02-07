from .Client import OpenHABClient

class ConfigDescriptions:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ConfigDescriptions class with an OpenHABClient instance.

        :param client: An instance of OpenHABClient used for REST API communication.
        """
        self.client = client

    def getAllConfigDescriptions(self, language: str = None, scheme: str = None) -> list:
        """
        Retrieves all available config descriptions.

        :param language: Optional header 'Accept-Language' to specify the preferred language.
        :param scheme: Optional query parameter to filter results by a specific scheme.

        :return: A list of configuration descriptions.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {}
        if scheme:
            params["scheme"] = scheme

        return self.client.get("/config-descriptions", header=header, params=params)

    def getConfigDescriptionByUri(self, uri: str, language: str = None) -> dict:
        """
        Retrieves a config description by URI.

        :param uri: The URI of the requested configuration description.
        :param language: Optional header 'Accept-Language' to specify the preferred language.

        :return: Details of the specific configuration description.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/config-descriptions/{uri}", header=header)

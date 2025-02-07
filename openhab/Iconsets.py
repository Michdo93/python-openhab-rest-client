from .Client import OpenHABClient

class Iconsets:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Iconsets class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllIconsets(self, language: str = None) -> list:
        """
        Gets all icon sets.

        :param language: Optional language preference for the response (e.g. 'en', 'de').
        
        :return: A list of icon sets with details such as ID, label, description and supported formats.
        """
        
        return self.client.get("/iconsets", header={"Accept-Language": language} if language else {})

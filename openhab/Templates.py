from .Client import OpenHABClient

class Templates:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Templates class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllTemplates(self, language: str = None) -> list:
        """
        Get all available templates.

        :param language: (Optional) Language setting for the Accept-Language header.
        :return: A list of templates.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get("/templates", header=header)

    def getTemplateByUID(self, templateUID: str, language: str = None) -> dict:
        """
        Gets a template corresponding to the given UID.

        :param templateUID: The UID of the template.
        :param language: (Optional) Language setting for the Accept-Language header.
        
        :return: A dictionary with the details of the template.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/templates/{templateUID}", header=header)

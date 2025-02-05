from .client import OpenHABClient

class ModuleTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ModuleTypes class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getModuleTypes(self, tags=None, typeFilter=None, language: str = None):
        """
        Get all available module types.

        :param tags: Optional filter for tags.
        :param typeFilter: Optional filter for the type (action, condition, trigger).
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of module types.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        params = {}
        if tags:
            params["tags"] = tags
        if typeFilter:
            params["type"] = typeFilter

        return self.client.get("/module-types", params=params, header=header)

    def getModuleType(self, moduleTypeUID, language: str = None):
        """
        Gets a module type corresponding to the given UID.

        :param moduleTypeUID: The UID of the module type.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A dictionary with the module type information.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/module-types/{moduleTypeUID}", header=header)

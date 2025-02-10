from .Client import OpenHABClient

class ThingTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ThingTypes class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllThingTypes(self, bindingId: str = None, language: str = None) -> list:
        """
        Gets all available thing types without config description, channels, and properties.

        :param bindingId: (Optional) Filter by binding ID.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of thing types.
        """
        params = {}
        if bindingId:
            params["bindingId"] = bindingId
        if language:
            header["Accept-Language"] = language

        return self.client.get("/thing-types", header={"Content-Type": "application/json"}, params=params)

    def getThingType(self, thingTypeUID: str, language: str = None) -> dict:
        """
        Gets a thing type by UID.

        :param thingTypeUID: The UID of the thing type.
        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A dictionary with the details of the thing type or an empty response with status 204.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/thing-types/{thingTypeUID}", header=header)

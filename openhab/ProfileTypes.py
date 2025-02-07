from .Client import OpenHABClient

class ProfileTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ProfileTypes class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getProfileTypes(self, channelTypeUID=None, itemType=None, language: str = None):
        """
        Gets all available profile types.

        :param channelTypeUID: Optional filter for the channel type.
        :param itemType: Optional filter for the item type.
        :param language: (Optional) Language setting for the Accept-Language header.
        
        :return: A list of profile types.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        params = {}
        if channelTypeUID:
            params["channelTypeUID"] = channelTypeUID
        if itemType:
            params["itemType"] = itemType

        return self.client.get("/profile-types", params=params, header=header)

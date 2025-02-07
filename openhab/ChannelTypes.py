from .Client import OpenHABClient

class ChannelTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ChannelTypes class with an OpenHABClient instance.

        :param client: An instance of OpenHABClient used for REST API communication.
        """
        self.client = client

    def getAllChannelTypes(self, language: str = None, prefixes: str = None) -> list:
        """
        Retrieves all available channel types.

        :param language: Optional header 'Accept-Language' to specify the preferred language.
        :param prefixes: Optional query parameter to filter channel types by prefix.

        :return: A list of channel types.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {}
        if prefixes:
            params["prefixes"] = prefixes

        return self.client.get("/channel-types", header=header, params=params)

    def getChannelTypeByUid(self, channelTypeUid: str, language: str = None) -> dict:
        """
        Retrieves the item types the given trigger channel type UID can be linked to.

        :param channelTypeUid: The unique UID of the channel type.
        :param language: Optional header 'Accept-Language' to specify the preferred language.

        :return: Details of the specific channel type.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/channel-types/{channelTypeUid}", header=header)

    def getLinkableItemTypes(self, channelTypeUid: str) -> list:
        """
        Retrieves the item types that can be linked to the specified trigger channel type.

        :param channelTypeUid: The unique UID of the channel type.

        :return: A list of item types.
        """
        return self.client.get(f"/channel-types/{channelTypeUid}/linkableItemTypes")

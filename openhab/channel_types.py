from .client import OpenHABClient

class ChannelTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die ChannelTypes-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_channel_types(self, language: str = None, prefixes: str = None) -> list:
        """
        Ruft alle verfügbaren Channel-Typen ab.

        :param language: Optionaler Header 'Accept-Language', um die bevorzugte Sprache anzugeben.
        :param prefixes: Optionaler Query-Parameter, um Channel-Typen nach Präfix zu filtern.
        :return: Eine Liste von Channel-Typen.
        """
        endpoint = "/channel-types"
        headers = {}
        if language:
            headers["Accept-Language"] = language

        params = {}
        if prefixes:
            params["prefixes"] = prefixes

        return self.client.get(endpoint, headers=headers, params=params)

    def get_channel_type_by_uid(self, channel_type_uid: str, language: str = None) -> dict:
        """
        Ruft einen spezifischen Channel-Typ anhand der UID ab.

        :param channel_type_uid: Die eindeutige UID des Channel-Typs.
        :param language: Optionaler Header 'Accept-Language', um die bevorzugte Sprache anzugeben.
        :return: Details des spezifischen Channel-Typs.
        """
        endpoint = f"/channel-types/{channel_type_uid}"
        headers = {}
        if language:
            headers["Accept-Language"] = language

        return self.client.get(endpoint, headers=headers)

    def get_linkable_item_types(self, channel_type_uid: str) -> list:
        """
        Ruft die Item-Typen ab, die mit dem angegebenen Trigger-Channel-Typ verknüpft werden können.

        :param channel_type_uid: Die eindeutige UID des Channel-Typs.
        :return: Eine Liste von Item-Typen.
        """
        endpoint = f"/channel-types/{channel_type_uid}/linkableItemTypes"
        return self.client.get(endpoint)

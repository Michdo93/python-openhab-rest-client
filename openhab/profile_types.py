from .client import OpenHABClient

class ProfileTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die ProfileTypes-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_profile_types(self, channel_type_uid=None, item_type=None, language: str = None):
        """
        Ruft alle verfügbaren Profiltypen ab.

        :param channel_type_uid: Optionaler Filter für den Kanaltyp.
        :param item_type: Optionaler Filter für den Elementtyp.
        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Eine Liste von Profiltypen.
        """
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        params = {}
        if channel_type_uid:
            params["channelTypeUID"] = channel_type_uid
        if item_type:
            params["itemType"] = item_type

        return self.client.get("/profile-types", params=params, header=header)

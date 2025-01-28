from .client import OpenHABClient

class ThingTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die ThingTypes-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_thing_types(self, binding_id: str = None, language: str = None) -> list:
        """
        Ruft alle verfügbaren Thing-Typen ohne Konfigurationsbeschreibung, Kanäle und Eigenschaften ab.

        :param binding_id: (Optional) Filter nach Binding-ID.
        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Eine Liste von Thing-Typen.
        :raises: Eine Exception, falls der Request fehlschlägt.
        """
        endpoint = "/thing-types"
        header = {"Content-Type": "application/json"}
        params = {}

        if binding_id:
            params["bindingId"] = binding_id
        if language:
            header["Accept-Language"] = language

        return self.client.get(endpoint, header=header, params=params)

    def get_thing_type(self, thing_type_uid: str, language: str = None) -> dict:
        """
        Ruft einen spezifischen Thing-Typ anhand seiner UID ab.

        :param thing_type_uid: Die UID des Thing-Typs.
        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Ein Dictionary mit den Details des Thing-Typs oder eine leere Antwort bei Status 204.
        :raises: Eine Exception, falls der Request fehlschlägt.
        """
        endpoint = f"/thing-types/{thing_type_uid}"
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get(endpoint, header=header)


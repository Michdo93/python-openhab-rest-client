from .client import OpenHABClient

class Things:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Things-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_things(self, summary: bool = False, static_data_only: bool = False, language: str = None):
        """
        Holt alle verfügbaren "Things".

        :param summary: Wenn True, gibt nur die Zusammenfassungsfelder zurück.
        :param static_data_only: Wenn True, gibt eine cachebare Liste zurück.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: JSON-Antwort mit den "Things".
        """
        params = {
            'summary': summary,
            'staticDataOnly': static_data_only
        }
        headers = {'Accept-Language': language} if language else {}
        return self.client.get('/things', params=params, headers=headers)

    def create_thing(self, thing_data: dict, language: str = None):
        """
        Erstellt ein neues Thing und fügt es dem Registry hinzu.

        :param thing_data: Das JSON-Objekt mit den Thing-Daten.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: Die Antwort der API.
        """
        headers = {'Accept-Language': language} if language else {}
        return self.client.post('/things', json=thing_data, headers=headers)

    def get_thing_by_uid(self, thing_uid: str, language: str = None):
        """
        Holt ein Thing anhand der UID.

        :param thing_uid: Die UID des Things.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: JSON-Antwort mit den Thing-Daten.
        """
        headers = {'Accept-Language': language} if language else {}
        return self.client.get(f'/things/{thing_uid}', headers=headers)

    def update_thing(self, thing_uid: str, thing_data: dict, language: str = None):
        """
        Aktualisiert ein Thing anhand der UID.

        :param thing_uid: Die UID des Things.
        :param thing_data: Das JSON-Objekt mit den aktualisierten Thing-Daten.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: Die Antwort der API.
        """
        headers = {'Accept-Language': language} if language else {}
        return self.client.put(f'/things/{thing_uid}', json=thing_data, headers=headers)

    def delete_thing(self, thing_uid: str, force: bool = False, language: str = None):
        """
        Entfernt ein Thing aus dem Registry.

        :param thing_uid: Die UID des Things.
        :param force: Wenn True, wird das Thing sofort entfernt.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: Die Antwort der API.
        """
        params = {'force': force}
        headers = {'Accept-Language': language} if language else {}
        return self.client.delete(f'/things/{thing_uid}', params=params, headers=headers)

    def update_thing_configuration(self, thing_uid: str, configuration_data: dict, language: str = None):
        """
        Aktualisiert die Konfiguration eines Things.

        :param thing_uid: Die UID des Things.
        :param configuration_data: Die Konfigurationsdaten des Things.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: Die Antwort der API.
        """
        headers = {'Accept-Language': language} if language else {}
        return self.client.put(f'/things/{thing_uid}/config', json=configuration_data, headers=headers)

    def enable_thing(self, thing_uid: str, enabled: bool, language: str = None):
        """
        Setzt den Status eines Things auf aktiviert oder deaktiviert.

        :param thing_uid: Die UID des Things.
        :param enabled: Wenn True, wird das Thing aktiviert.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: Die Antwort der API.
        """
        data = {'enabled': str(enabled).lower()}
        headers = {'Accept-Language': language} if language else {}
        return self.client.put(f'/things/{thing_uid}/enable', json=data, headers=headers)

    def get_thing_status(self, thing_uid: str, language: str = None):
        """
        Holt den Status eines Things.

        :param thing_uid: Die UID des Things.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: Die Antwort mit dem Status des Things.
        """
        headers = {'Accept-Language': language} if language else {}
        return self.client.get(f'/things/{thing_uid}/status', headers=headers)
    
    def get_thing_firmware_status(self, thing_uid: str, language: str = None):
        """
        Holt den Firmware-Status eines Things.

        :param thing_uid: Die UID des Things.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: JSON-Antwort mit dem Firmware-Status.
        """
        headers = {'Accept-Language': language} if language else {}
        return self.client.get(f'/things/{thing_uid}/firmware/status', headers=headers)

    def update_thing_firmware(self, thing_uid: str, firmware_version: str, language: str = None):
        """
        Aktualisiert die Firmware eines Things.

        :param thing_uid: Die UID des Things.
        :param firmware_version: Die Firmware-Version.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: Die Antwort der API.
        """
        headers = {'Accept-Language': language} if language else {}
        return self.client.put(f'/things/{thing_uid}/firmware/{firmware_version}', headers=headers)

    def get_thing_firmwares(self, thing_uid: str, language: str = None):
        """
        Holt alle verfügbaren Firmwares für ein Thing.

        :param thing_uid: Die UID des Things.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: Die Liste der verfügbaren Firmwares.
        """
        headers = {'Accept-Language': language} if language else {}
        return self.client.get(f'/things/{thing_uid}/firmwares', headers=headers)

    def get_thing_config_status(self, thing_uid: str, language: str = None):
        """
        Holt den Konfigurationsstatus eines Things.

        :param thing_uid: Die UID des Things.
        :param language: Die bevorzugte Sprache für die Antwort.
        :return: JSON-Antwort mit dem Konfigurationsstatus des Things.
        """
        headers = {'Accept-Language': language} if language else {}
        return self.client.get(f'/things/{thing_uid}/config/status', headers=headers)

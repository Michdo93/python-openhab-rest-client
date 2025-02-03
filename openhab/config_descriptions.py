from .client import OpenHABClient


class ConfigDescriptions:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die ConfigDescriptions-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_config_descriptions(self, language: str = None, scheme: str = None) -> list:
        """
        Ruft alle verfügbaren Konfigurationsbeschreibungen ab.

        :param language: Optionaler Header 'Accept-Language', um die bevorzugte Sprache anzugeben.
        :param scheme: Optionaler Query-Parameter, um die Ergebnisse nach einem bestimmten Schema zu filtern.
        :return: Eine Liste von Konfigurationsbeschreibungen.
        """
        endpoint = "/config-descriptions"
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {}
        if scheme:
            params["scheme"] = scheme

        return self.client.get(endpoint, header=header, params=params)

    def get_config_description_by_uri(self, uri: str, language: str = None) -> dict:
        """
        Ruft eine spezifische Konfigurationsbeschreibung anhand der URI ab.

        :param uri: Die URI der gewünschten Konfigurationsbeschreibung.
        :param language: Optionaler Header 'Accept-Language', um die bevorzugte Sprache anzugeben.
        :return: Details der spezifischen Konfigurationsbeschreibung.
        :raises ValueError: Wenn die URI ungültig ist oder nicht gefunden wird.
        """
        endpoint = f"/config-descriptions/{uri}"
        header = {}
        if language:
            header["Accept-Language"] = language

        try:
            return self.client.get(endpoint, header=header)
        except Exception as e:
            if "400" in str(e):
                raise ValueError("Ungültige URI-Syntax.")
            elif "404" in str(e):
                raise ValueError("URI nicht gefunden.")
            else:
                raise

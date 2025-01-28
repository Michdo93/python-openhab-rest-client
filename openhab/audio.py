from .client import OpenHABClient

class Audio:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Audio-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_default_sink(self, language: str = None):
        """
        Ruft das Standard-Audio-Sink ab.

        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Ein Dictionary mit Informationen über das Standard-Sink.
        """
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get("/audio/defaultsink", header=header)

    def get_default_source(self, language: str = None):
        """
        Ruft die Standard-Audio-Quelle ab.

        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Ein Dictionary mit Informationen über die Standard-Quelle.
        """
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get("/audio/defaultsource", header=header)

    def get_sinks(self, language: str = None):
        """
        Ruft eine Liste aller verfügbaren Audio-Sinks ab.

        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Eine Liste von Sinks.
        """
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get("/audio/sinks", header=header)

    def get_sources(self, language: str = None):
        """
        Ruft eine Liste aller verfügbaren Audio-Quellen ab.

        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Eine Liste von Quellen.
        """
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get("/audio/sources", header=header)

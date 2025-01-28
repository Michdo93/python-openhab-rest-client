from .client import OpenHABClient


class Events:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Events-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_events(self, topics: str = None) -> list:
        """
        Ruft alle verfügbaren Events ab, optional gefiltert nach Themen (Topics).

        :param topics: Eine durch Kommas getrennte Liste von Topics zum Filtern der Events.
        :return: Eine Liste von Events.
        :raises ValueError: Wenn das angegebene Topic leer oder ungültig ist.
        """
        endpoint = "/events"
        params = {"topics": topics} if topics else {}
        try:
            return self.client.get(endpoint, params=params)
        except Exception as e:
            raise ValueError(f"Ungültige oder leere Topics: {e}")

    def initiate_state_tracker(self) -> str:
        """
        Startet eine neue Verbindung zum Verfolgen von Item-Statusänderungen.

        :return: Die Verbindungs-ID als String.
        """
        endpoint = "/events/states"
        return self.client.get(endpoint)

    def update_sse_connection_items(self, connection_id: str, items: list) -> str:
        """
        Aktualisiert die Liste von Items, für die eine SSE-Verbindung Statusaktualisierungen erhält.

        :param connection_id: Die ID der bestehenden Verbindung.
        :param items: Eine Liste von Item-Namen, für die Statusaktualisierungen abonniert werden sollen.
        :return: Eine Erfolgsnachricht, wenn die Aktualisierung abgeschlossen ist.
        :raises ValueError: Wenn die Verbindung oder die Liste der Items ungültig ist.
        """
        if not connection_id:
            raise ValueError("Die Verbindungs-ID darf nicht leer sein.")
        if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
            raise ValueError("Die Items-Liste muss eine Liste von Strings sein.")

        endpoint = f"/events/states/{connection_id}"
        payload = items
        try:
            return self.client.post(endpoint, json=payload)
        except Exception as e:
            raise ValueError(f"Fehler beim Aktualisieren der Verbindung: {e}")

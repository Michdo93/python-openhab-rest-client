from .client import OpenHABClient

class Discovery:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Discovery-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_discovery_bindings(self) -> list:
        """
        Ruft alle Bindings ab, die die Discovery-Funktion unterstützen.

        :return: Eine Liste der Bindings als Strings.
        """
        endpoint = "/discovery"
        return self.client.get(endpoint)

    def start_binding_scan(self, binding_id: str) -> int:
        """
        Startet den asynchronen Discovery-Prozess für ein Binding und gibt die Timeout-Dauer in Sekunden zurück.

        :param binding_id: Die ID des Bindings, für das die Discovery gestartet werden soll.
        :return: Timeout-Dauer der Discovery-Operation in Sekunden.
        :raises ValueError: Wenn die Binding-ID nicht angegeben oder leer ist.
        """
        if not binding_id:
            raise ValueError("Die Binding-ID muss angegeben werden.")
        
        endpoint = f"/discovery/bindings/{binding_id}/scan"
        response = self.client.post(endpoint)
        return response  # Erwartet, dass die Antwort ein Integer ist (Timeout in Sekunden).

from .client import OpenHABClient

class Logging:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Logging-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_loggers(self) -> dict:
        """
        Ruft alle Loggers ab.

        :return: Eine Liste von Loggers mit Namen und Level.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = "/logging"
        
        try:
            return self.client.get(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen der Loggers: {e}")

    def get_single_logger(self, logger_name: str) -> dict:
        """
        Ruft einen einzelnen Logger anhand des Logger-Namens ab.

        :param logger_name: Der Name des Loggers.
        :return: Der Logger mit dem angegebenen Namen und Level.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/logging/{logger_name}"
        
        try:
            return self.client.get(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen des Loggers: {e}")

    def modify_or_add_logger(self, logger_name: str, level: str) -> dict:
        """
        Modifiziert oder fügt einen Logger hinzu.

        :param logger_name: Der Name des Loggers.
        :param level: Das Level des Loggers.
        :return: Die Antwort der API nach der Modifikation oder Hinzufügung.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/logging/{logger_name}"
        data = {
            "loggerName": logger_name,
            "level": level
        }
        
        try:
            return self.client.put(endpoint, json=data)
        except Exception as e:
            raise Exception(f"Fehler beim Modifizieren oder Hinzufügen des Loggers: {e}")

    def remove_logger(self, logger_name: str) -> dict:
        """
        Entfernt einen Logger.

        :param logger_name: Der Name des Loggers.
        :return: Die Antwort der API nach dem Entfernen des Loggers.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/logging/{logger_name}"
        
        try:
            return self.client.delete(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Entfernen des Loggers: {e}")

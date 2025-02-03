from .client import OpenHABClient
import json

class Persistence:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Persistence-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_services(self) -> dict:
        """
        Ruft alle Persistence-Dienste ab.

        :return: Eine Liste der Persistence-Dienste mit IDs, Labels und Typen.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = "/persistence"
        
        try:
            return self.client.get(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen der Persistence-Dienste: {e}")

    def get_service_configuration(self, service_id: str) -> dict:
        """
        Ruft die Konfiguration eines bestimmten Persistence-Dienstes ab.

        :param service_id: Die ID des Persistence-Dienstes.
        :return: Die Konfiguration des Dienstes.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/persistence/{service_id}"
        
        try:
            return self.client.get(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen der Konfiguration des Persistence-Dienstes: {e}")

    def set_service_configuration(self, service_id: str, config: dict) -> dict:
        """
        Setzt die Konfiguration für einen bestimmten Persistence-Dienst.

        :param service_id: Die ID des Persistence-Dienstes.
        :param config: Die Konfigurationsdaten.
        :return: Die Antwort der API nach der Modifikation.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/persistence/{service_id}"
        
        # Header für die Anfrage
        header = {
            "Content-Type": "application/json",  # Senden von JSON-Daten im Body
            "Accept": "application/json"          # Erwartung einer JSON-Antwort
        }

        # Füge das serviceId-Feld zu den Konfigurationsdaten hinzu
        config['serviceId'] = service_id

        data = json.dumps(config)

        try:
            # Verwende json=config, um sicherzustellen, dass die Daten korrekt serialisiert werden
            return self.client.put(endpoint, data=data, header=header)
        except Exception as e:
            raise Exception(f"Fehler beim Setzen der Konfiguration des Persistence-Dienstes: {e}")


    def delete_service_configuration(self, service_id: str) -> dict:
        """
        Löscht die Konfiguration eines Persistence-Dienstes.

        :param service_id: Die ID des Persistence-Dienstes.
        :return: Die Antwort der API nach dem Löschen der Konfiguration.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/persistence/{service_id}"
        
        try:
            return self.client.delete(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Löschen der Konfiguration des Persistence-Dienstes: {e}")

    def get_items_for_service(self, service_id: str) -> dict:
        """
        Ruft eine Liste von Items ab, die über einen bestimmten Persistence-Dienst verfügbar sind.

        :param service_id: Die ID des Persistence-Dienstes.
        :return: Eine Liste von Items mit ihren letzten und frühesten Zeitstempeln.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/persistence/items?serviceId={service_id}"
        
        try:
            return self.client.get(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen der Items für den Persistence-Dienst: {e}")

    def get_item_persistence_data(self, service_id: str, item_name: str, start_time: str = None, end_time: str = None, page: int = 1, page_length: int = 50) -> dict:
        """
        Ruft die Persistence-Daten für ein bestimmtes Item aus einem Persistence-Dienst ab.

        :param service_id: Die ID des Persistence-Dienstes.
        :param item_name: Der Name des Items.
        :param start_time: Der Startzeitpunkt für die Daten. Standardmäßig 1 Tag vor `end_time`.
        :param end_time: Der Endzeitpunkt für die Daten. Standardmäßig die aktuelle Zeit.
        :param page: Die Seite der Daten. Standardmäßig `1`.
        :param page_length: Die Anzahl der Datenpunkte pro Seite. Standardmäßig `50`.
        :return: Die abgerufenen Datenpunkte des Items.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/persistence/items/{item_name}"
        params = {
            "serviceId": service_id,
            "starttime": start_time,
            "endtime": end_time,
            "page": page,
            "pagelength": page_length
        }

        try:
            return self.client.get(endpoint, params=params)
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen der Persistence-Daten für Item {item_name}: {e}")

    def store_item_data(self, service_id: str, item_name: str, time: str, state: str) -> dict:
        """
        Speichert Persistence-Daten für ein bestimmtes Item in einem Persistence-Dienst.

        :param service_id: Die ID des Persistence-Dienstes.
        :param item_name: Der Name des Items.
        :param time: Der Zeitpunkt der Speicherung.
        :param state: Der zu speichernde Zustand des Items.
        :return: Die Antwort der API nach dem Speichern der Daten.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/persistence/items/{item_name}"

        # Query-Parameter (nicht im Body, sondern in der URL)
        params = {
            "serviceId": service_id,  # Optional, wenn kein Default-Service vorhanden ist
            "time": time,  # Zeit der Speicherung
            "state": state  # Zustand des Items
        }

        # Absenden der PUT-Anfrage mit den Query-Parametern
        try:
            response = self.client.put(endpoint, params=params)
            return response
        except Exception as e:
            raise Exception(f"Fehler beim Speichern der Persistence-Daten für Item {item_name}: {e}")


    def delete_item_data(self, service_id: str, item_name: str, start_time: str, end_time: str) -> dict:
        """
        Löscht Persistence-Daten für ein bestimmtes Item aus einem Persistence-Dienst innerhalb eines angegebenen Zeitraums.

        :param service_id: Die ID des Persistence-Dienstes.
        :param item_name: Der Name des Items.
        :param start_time: Der Startzeitpunkt der zu löschenden Daten.
        :param end_time: Der Endzeitpunkt der zu löschenden Daten.
        :return: Die Antwort der API nach dem Löschen der Daten.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/persistence/items/{item_name}"
        params = {
            "serviceId": service_id,
            "starttime": start_time,
            "endtime": end_time
        }

        try:
            return self.client.delete(endpoint, params=params)
        except Exception as e:
            raise Exception(f"Fehler beim Löschen der Persistence-Daten für Item {item_name}: {e}")

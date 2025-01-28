from .client import OpenHABClient
import requests

class Rules:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Rules-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_rules(self, prefix=None, tags=None, summary=False, static_data_only=False):
        """
        Holt alle verfügbaren Regeln. Es können optional Filter wie Präfix und Tags gesetzt werden.

        :param prefix: Optionales Präfix, um die Ergebnisse zu filtern.
        :param tags: Optionales Tag-Array, um die Ergebnisse zu filtern.
        :param summary: Wenn wahr, werden nur Zusammenfassungsfelder zurückgegeben.
        :param static_data_only: Wenn wahr, wird nur statisches Datenmaterial zurückgegeben.

        :return: Eine Liste von Regeln (JSON-Objekten).
        """
        params = {
            "prefix": prefix,
            "tags": tags,
            "summary": summary,
            "staticDataOnly": static_data_only
        }
        return self.client.get("/rules", params=params)

    def get_rule(self, rule_uid: str):
        """
        Holt eine spezifische Regel anhand ihrer UID.

        :param rule_uid: Die UID der zu holenden Regel.

        :return: Das Regel-Objekt (JSON).
        """
        return self.client.get(f"/rules/{rule_uid}")

    def create_rule(self, rule_data: dict):
        """
        Erstellt eine neue Regel mit den gegebenen Daten.

        :param rule_data: Die zu erstellenden Regeldaten (als Dictionary).

        :return: Die erstellte Regel (JSON).
        """
        return self.client.post("/rules", json=rule_data)

    def update_rule(self, rule_uid: str, rule_data: dict):
        """
        Aktualisiert eine bestehende Regel anhand ihrer UID.

        :param rule_uid: Die UID der zu aktualisierenden Regel.
        :param rule_data: Die neuen Regeldaten (als Dictionary).

        :return: Die aktualisierte Regel (JSON).
        """
        return self.client.put(f"/rules/{rule_uid}", json=rule_data)

    def delete_rule(self, rule_uid: str):
        """
        Löscht eine Regel anhand ihrer UID.

        :param rule_uid: Die UID der zu löschenden Regel.

        :return: Die Antwort der API (Statuscode).
        """
        return self.client.delete(f"/rules/{rule_uid}")

    def get_triggers(self, rule_uid: str):
        """
        Holt alle Trigger einer Regel anhand ihrer UID.

        :param rule_uid: Die UID der Regel.

        :return: Eine Liste der Trigger (JSON).
        """
        return self.client.get(f"/rules/{rule_uid}/triggers")

    def get_conditions(self, rule_uid: str):
        """
        Holt alle Bedingungen einer Regel anhand ihrer UID.

        :param rule_uid: Die UID der Regel.

        :return: Eine Liste der Bedingungen (JSON).
        """
        return self.client.get(f"/rules/{rule_uid}/conditions")

    def get_actions(self, rule_uid: str):
        """
        Holt alle Aktionen einer Regel anhand ihrer UID.

        :param rule_uid: Die UID der Regel.

        :return: Eine Liste der Aktionen (JSON).
        """
        return self.client.get(f"/rules/{rule_uid}/actions")

    def get_configuration(self, rule_uid: str):
        """
        Holt die Konfiguration einer Regel anhand ihrer UID.

        :param rule_uid: Die UID der Regel.

        :return: Die Konfiguration der Regel (JSON).
        """
        return self.client.get(f"/rules/{rule_uid}/config")

    def update_configuration(self, rule_uid: str, config_data: dict):
        """
        Aktualisiert die Konfiguration einer Regel anhand ihrer UID.

        :param rule_uid: Die UID der Regel.
        :param config_data: Die neuen Konfigurationsdaten (als Dictionary).

        :return: Die aktualisierte Konfiguration (JSON).
        """
        return self.client.put(f"/rules/{rule_uid}/config", json=config_data)

    def enable_rule(self, rule_uid: str, enable: bool):
        """
        Aktiviert oder deaktiviert eine Regel.

        :param rule_uid: Die UID der Regel.
        :param enable: Wenn wahr, wird die Regel aktiviert. Wenn falsch, wird die Regel deaktiviert.

        :return: Die Antwort der API (Statuscode).
        """
        return self.client.post(f"/rules/{rule_uid}/enable", json={"enable": "true" if enable else "false"})

    def run_now(self, rule_uid: str, context_data: dict = None):
        """
        Führt sofort die Aktionen einer Regel aus.

        :param rule_uid: Die UID der Regel.
        :param context_data: Optionale Kontextdaten für die Ausführung der Regel.

        :return: Die Antwort der API (Statuscode).
        """
        return self.client.post(f"/rules/{rule_uid}/runnow", json=context_data or {})



    def get_module(self, rule_uid: str, module_category: str, module_id: str):
        """
        Holt ein bestimmtes Modul einer Regel.

        :param rule_uid: Die UID der Regel.
        :param module_category: Die Kategorie des Moduls.
        :param module_id: Die ID des Moduls.

        :return: Das Modul (JSON).
        """
        return self.client.get(f"/rules/{rule_uid}/{module_category}/{module_id}")

    def get_module_config(self, rule_uid: str, module_category: str, module_id: str):
        """
        Holt die gesamte Konfiguration eines Moduls einer Regel.

        :param rule_uid: Die UID der Regel.
        :param module_category: Die Kategorie des Moduls.
        :param module_id: Die ID des Moduls.

        :return: Die Konfiguration des Moduls (JSON).
        """
        return self.client.get(f"/rules/{rule_uid}/{module_category}/{module_id}/config")

    def get_module_config_param(self, rule_uid: str, module_category: str, module_id: str, param: str):
        """
        Holt einen spezifischen Konfigurationsparameter eines Moduls einer Regel.

        :param rule_uid: Die UID der Regel.
        :param module_category: Die Kategorie des Moduls.
        :param module_id: Die ID des Moduls.
        :param param: Der Name des Konfigurationsparameters.

        :return: Der Wert des Konfigurationsparameters (JSON).
        """
        return self.client.get(f"/rules/{rule_uid}/{module_category}/{module_id}/config/{param}")

    def set_module_config_param(self, rule_uid: str, module_category: str, module_id: str, param: str, value: str):
        """
        Setzt einen spezifischen Konfigurationsparameter eines Moduls einer Regel.

        :param rule_uid: Die UID der Regel.
        :param module_category: Die Kategorie des Moduls.
        :param module_id: Die ID des Moduls.
        :param param: Der Name des Konfigurationsparameters.
        :param value: Der zu setzende Wert des Konfigurationsparameters.

        :return: Die Antwort der API (Statuscode).
        """
        return self.client.put(f"/rules/{rule_uid}/{module_category}/{module_id}/config/{param}", json=value)

    def simulate_schedule(self, from_time: str, until_time: str):
        """
        Simuliert die Ausführung von Zeitplan-Regeln in einem bestimmten Zeitraum.

        :param from_time: Der Startzeitpunkt der Simulation.
        :param until_time: Der Endzeitpunkt der Simulation.

        :return: Die Simulationsergebnisse (JSON).
        """
        params = {
            "from": from_time,
            "until": until_time
        }
        return self.client.get("/rules/schedule/simulations", params=params)

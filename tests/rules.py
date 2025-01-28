import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Rules

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
rules_api = Rules(client)

# Beispiele für die Rules-API
def rules_examples():
    # Alle Regeln abrufen
    all_rules = rules_api.get_all_rules()
    print("All Rules:", all_rules)

    # Details zu einer Regel abrufen
    test_rule = rules_api.get_rule("testRule")
    print("testRule Details:", test_rule)

    # Neue Regel hinzufügen oder aktualisieren
    new_rule_data = {
        "uid": "newRule",
        "name": "New Rule",
        "description": "This is a new rule",
        "triggers": [],
        "conditions": [],
        "actions": []
    }
    rules_api.add_or_update_rule("newRule", new_rule_data)
    print("New Rule added/updated.")

    # Regel aktivieren
    rules_api.enable_rule("newRule")
    print("newRule enabled.")

    # Regel deaktivieren
    rules_api.disable_rule("newRule")
    print("newRule disabled.")

    # Regel löschen
    rules_api.delete_rule("newRule")
    print("newRule deleted.")

    # Beispiel-Regel-UID, Kategorie und Modul-ID
    rule_uid = "exampleRule"
    module_category = "actions"
    module_id = "exampleModule"

    # Modul abrufen
    module = rules_api.get_module(rule_uid, module_category, module_id)
    print("Modul:", module)

    # Modulkonfiguration abrufen
    module_config = rules_api.get_module_config(rule_uid, module_category, module_id)
    print("Modulkonfiguration:", module_config)

    # Spezifischen Konfigurationsparameter abrufen
    param_name = "exampleParam"
    param_value = rules_api.get_module_config_param(rule_uid, module_category, module_id, param_name)
    print(f"Wert des Parameters '{param_name}':", param_value)

    # Spezifischen Konfigurationsparameter setzen
    new_value = "newValue"
    response = rules_api.set_module_config_param(rule_uid, module_category, module_id, param_name, new_value)
    print(f"Parameter '{param_name}' auf Wert '{new_value}' gesetzt:", response)

# Funktion ausführen
if __name__ == "__main__":
    rules_examples()

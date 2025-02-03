import sys
import os
import time

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Rules

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
rules_api = Rules(client)

def rules_examples():
    try:
        # Alle Regeln abrufen
        all_rules = rules_api.get_rules()
        print("All Rules:", all_rules)
    except Exception as e:
        print("Error getting all rules:", e)
    
    try:
        # Details zu einer Regel abrufen
        test_rule = rules_api.get_rule("test_color-1")
        print("testRule Details:", test_rule)
    except Exception as e:
        print("Error getting rule details:", e)
    
    try:
        # Neue Regel hinzufügen
        new_rule_data = {
            "uid": "newRule",
            "name": "New Rule",
            "description": "This is a new rule",
            "triggers": [],
            "conditions": [],
            "actions": []
        }
        rules_api.create_rule(new_rule_data)
        print("New Rule created.")
    except Exception as e:
        print("Error creating rule:", e)
    
    try:
        # Regel aktualisieren
        updated_rule_data = {"name": "Updated Rule"}
        rules_api.update_rule("newRule", updated_rule_data)
        print("Rule updated.")
    except Exception as e:
        print("Error updating rule:", e)
    
    try:
        # Regel aktivieren
        rules_api.set_rule_state("newRule", True)
        print("newRule enabled.")
    except Exception as e:
        print("Error enabling rule:", e)
    
    try:
    #    # Regel deaktivieren
        rules_api.set_rule_state("newRule", False)
        print("newRule disabled.")
    except Exception as e:
        print("Error disabling rule:", e)
    
    try:
        # Regel löschen
        rules_api.delete_rule("newRule")
        print("newRule deleted.")
    except Exception as e:
        print("Error deleting rule:", e)

    try:
        # Triggers abrufen
        triggers = rules_api.get_triggers("test_color-1")
        print("Triggers:", triggers)
    except Exception as e:
        print("Error getting triggers:", e)
    
    try:
        # Bedingungen abrufen
        conditions = rules_api.get_conditions("test_color-1")
        print("Conditions:", conditions)
    except Exception as e:
        print("Error getting conditions:", e)
    
    try:
        # Aktionen abrufen
        actions = rules_api.get_actions("test_color-1")
        print("Actions:", actions)
    except Exception as e:
        print("Error getting actions:", e)
    
    try:
        # Regelkonfiguration abrufen
        config = rules_api.get_configuration("test_color-1")
        print("Configuration:", config)
    except Exception as e:
        print("Error getting configuration:", e)
    
    try:
        # Regelkonfiguration aktualisieren
        rules_api.update_configuration("test_color-1", {"param": "value"})
        print("Configuration updated.")
    except Exception as e:
        print("Error updating configuration:", e)
    
    try:
        # Regel sofort ausführen
        rules_api.run_now("test_color-1")
        print("Rule executed immediately.")
    except Exception as e:
        print("Error running rule:", e)
    
    try:
        # Modul abrufen
        module = rules_api.get_module("test_color-1", "actions", "script")
        print("Module:", module)
    except Exception as e:
        print("Error getting module:", e)
    
    try:
        # Modulkonfiguration abrufen
        module_config = rules_api.get_module_config("test_color-1", "actions", "script")
        print("Module Configuration:", module_config)
    except Exception as e:
        print("Error getting module configuration:", e)

    try:
        # Modul-Konfigurationsparameter abrufen
        param_value = rules_api.get_module_config_param("test_color-1", "actions", "script", "exampleParam")
        print("Module Config Param:", param_value)
    except Exception as e:
        print("Error getting module config param:", e)

    try:
        # Modul-Konfigurationsparameter setzen
        rules_api.set_module_config_param("test_color-1", "actions", "script", "exampleParam", "newValue")
        print("Module Config Param updated.")
    except Exception as e:
        print("Error setting module config param:", e)
    
    try:
        # Zeitplansimulation ausführen
        simulation_result = rules_api.simulate_schedule("2025-02-03T10:20:00.987Z", "2025-02-03T10:38:00.987Z")
        print("Schedule Simulation Result:", simulation_result)
    except Exception as e:
        print("Error simulating schedule:", e)

# Funktion ausführen
if __name__ == "__main__":
    rules_examples()

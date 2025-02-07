import sys
import os
import time

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Rules

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
rulesApi = Rules(client)

def rulesExamples():
    try:
        # Alle Regeln abrufen
        allRules = rulesApi.getRules()
        print("All Rules:", allRules)
    except Exception as e:
        print("Error getting all rules:", e)
    
    try:
        # Details zu einer Regel abrufen
        testRule = rulesApi.getRule("test_color-1")
        print("testRule Details:", testRule)
    except Exception as e:
        print("Error getting rule details:", e)
    
    try:
        # Neue Regel hinzufügen
        newRuleData = {
            "uid": "newRule",
            "name": "New Rule",
            "description": "This is a new rule",
            "triggers": [],
            "conditions": [],
            "actions": []
        }
        rulesApi.createRule(newRuleData)
        print("New Rule created.")
    except Exception as e:
        print("Error creating rule:", e)
    
    try:
        # Regel aktualisieren
        updatedRuleData = {"name": "Updated Rule"}
        rulesApi.updateRule("newRule", updatedRuleData)
        print("Rule updated.")
    except Exception as e:
        print("Error updating rule:", e)
    
    try:
        # Regel aktivieren
        rulesApi.setRuleState("newRule", True)
        print("newRule enabled.")
    except Exception as e:
        print("Error enabling rule:", e)
    
    try:
        # Regel deaktivieren
        rulesApi.setRuleState("newRule", False)
        print("newRule disabled.")
    except Exception as e:
        print("Error disabling rule:", e)
    
    try:
        # Regel löschen
        rulesApi.deleteRule("newRule")
        print("newRule deleted.")
    except Exception as e:
        print("Error deleting rule:", e)

    try:
        # Triggers abrufen
        triggers = rulesApi.getTriggers("test_color-1")
        print("Triggers:", triggers)
    except Exception as e:
        print("Error getting triggers:", e)
    
    try:
        # Bedingungen abrufen
        conditions = rulesApi.getConditions("test_color-1")
        print("Conditions:", conditions)
    except Exception as e:
        print("Error getting conditions:", e)
    
    try:
        # Aktionen abrufen
        actions = rulesApi.getActions("test_color-1")
        print("Actions:", actions)
    except Exception as e:
        print("Error getting actions:", e)
    
    try:
        # Regelkonfiguration abrufen
        config = rulesApi.getConfiguration("test_color-1")
        print("Configuration:", config)
    except Exception as e:
        print("Error getting configuration:", e)
    
    try:
        # Regelkonfiguration aktualisieren
        rulesApi.updateConfiguration("test_color-1", {"param": "value"})
        print("Configuration updated.")
    except Exception as e:
        print("Error updating configuration:", e)
    
    try:
        # Regel sofort ausführen
        rulesApi.runNow("test_color-1")
        print("Rule executed immediately.")
    except Exception as e:
        print("Error running rule:", e)
    
    try:
        # Modul abrufen
        module = rulesApi.getModule("test_color-1", "actions", "script")
        print("Module:", module)
    except Exception as e:
        print("Error getting module:", e)
    
    try:
        # Modulkonfiguration abrufen
        moduleConfig = rulesApi.getModuleConfig("test_color-1", "actions", "script")
        print("Module Configuration:", moduleConfig)
    except Exception as e:
        print("Error getting module configuration:", e)

    try:
        # Modul-Konfigurationsparameter abrufen
        paramValue = rulesApi.getModuleConfigParam("test_color-1", "actions", "script", "exampleParam")
        print("Module Config Param:", paramValue)
    except Exception as e:
        print("Error getting module config param:", e)

    try:
        # Modul-Konfigurationsparameter setzen
        rulesApi.setModuleConfigParam("test_color-1", "actions", "script", "exampleParam", "newValue")
        print("Module Config Param updated.")
    except Exception as e:
        print("Error setting module config param:", e)
    
    try:
        # Zeitplansimulation ausführen
        simulationResult = rulesApi.simulateSchedule("2025-02-03T10:20:00.987Z", "2025-02-03T10:38:00.987Z")
        print("Schedule Simulation Result:", simulationResult)
    except Exception as e:
        print("Error simulating schedule:", e)

# Funktion ausführen
if __name__ == "__main__":
    rulesExamples()

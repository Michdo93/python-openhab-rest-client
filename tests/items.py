import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Items

# Client initialisieren (ersetze 'http://openhab-url' mit deiner URL und 'auth_token' mit deinem Token)
#client = OpenHABClient(base_url='http://openhab-url', auth_token='your_auth_token')
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
itemsApi = Items(client)

# Beispiele für jede Methode in Items
def examples():
    
    # Alle Items abrufen
    allItems = itemsApi.getAllItems()
    print("All Items:", allItems)

    
    # Ein einzelnes Item abrufen
    testSwitch = itemsApi.getItem("testSwitch")
    print("testSwitch Details:", testSwitch)
    
    # Neues Item hinzufügen oder aktualisieren
    newItemData = {
        "type": "Switch",
        "name": "newSwitch",
        "label": "New Switch",
        "groupNames": ["Static"],
        "tags": ["SwitchTag"],
        "category": "Switch"
    }
    itemsApi.addOrUpdateItem("newSwitch", newItemData)
    print("New Switch added/updated.")
    
    # Liste von Items hinzufügen oder aktualisieren
    newItems = [
        {
            "type": "Number",
            "name": "newNumber",
            "label": "New Number",
            "groupNames": ["Static"],
            "tags": ["NumberTag"],
            "category": "Number"
        },
        {
            "type": "String",
            "name": "newString",
            "label": "New String",
            "groupNames": ["Static"],
            "tags": ["StringTag"],
            "category": "String"
        }
    ]
    itemsApi.addOrUpdateItems(newItems)
    print("New Items added/updated.")
    
    # Befehl an ein Item senden
    itemsApi.sendCommand("testSwitch", "ON")
    print("Command sent to testSwitch.")

    # Zustand eines Items aktualisieren
    itemsApi.updateItemState("testNumber", "42")
    print("State of testNumber updated.")

    # Zustand eines Items abrufen
    testSwitchState = itemsApi.getItemState("testSwitch")
    print("testSwitch State:", testSwitchState)

    # Ein Item löschen
    itemsApi.deleteItem("newSwitch")
    print("newSwitch deleted.")

    # Gruppenmitglied hinzufügen
    itemsApi.addGroupMember("Static", "newNumber")
    print("newNumber added to Static group.")

    # Gruppenmitglied entfernen
    itemsApi.removeGroupMember("Static", "newNumber")
    print("newNumber removed from Static group.")
    
    # Metadaten hinzufügen
    metadata = {
        "value": "metadata_value",
        "config": {
            "key1": "value1",
            "key2": "value2"
        }
    }
    itemsApi.addMetadata("testSwitch", "exampleNamespace", metadata)
    print("Metadata added to testSwitch.")

    # Metadaten entfernen
    itemsApi.removeMetadata("testSwitch", "exampleNamespace")
    print("Metadata removed from testSwitch.")

    # Metadaten-Namespaces eines Items abrufen
    metadataNamespaces = itemsApi.getMetadataNamespaces("testSwitch")
    print("Metadata namespaces for testSwitch:", metadataNamespaces)
    
    # Item mit semantischer Klasse abrufen
    #semanticItem = itemsApi.getSemanticItem("testLocation", "Location")
    #print("Semantic item for testLocation:", semanticItem)

    # Einem Item ein Tag hinzufügen
    #itemsApi.addTag("testSwitch", "NewTag")
    #print("Tag added to testSwitch.")

    # Einem Item ein Tag entfernen
    #itemsApi.removeTag("testSwitch", "NewTag")
    #print("Tag removed from testSwitch.")

    # Verwaiste Metadaten löschen
    itemsApi.purgeOrphanedMetadata()
    print("Orphaned metadata purged.")
    
# Funktion ausführen
if __name__ == "__main__":
    examples()

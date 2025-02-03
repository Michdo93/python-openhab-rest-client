import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Items

# Client initialisieren (ersetze 'http://openhab-url' mit deiner URL und 'auth_token' mit deinem Token)
#client = OpenHABClient(base_url='http://openhab-url', auth_token='your_auth_token')
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
items_api = Items(client)

# Beispiele für jede Methode in Items
def examples():
    
    # Alle Items abrufen
    all_items = items_api.get_all_items()
    print("All Items:", all_items)

    
    # Ein einzelnes Item abrufen
    test_switch = items_api.get_item("testSwitch")
    print("testSwitch Details:", test_switch)
    
    # Neues Item hinzufügen oder aktualisieren
    new_item_data = {
        "type": "Switch",
        "name": "newSwitch",
        "label": "New Switch",
        "groupNames": ["Static"],
        "tags": ["SwitchTag"],
        "category": "Switch"
    }
    items_api.add_or_update_item("newSwitch", new_item_data)
    print("New Switch added/updated.")
    
    # Liste von Items hinzufügen oder aktualisieren
    new_items = [
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
    items_api.add_or_update_items(new_items)
    print("New Items added/updated.")
    
    # Befehl an ein Item senden
    items_api.send_command("testSwitch", "ON")
    print("Command sent to testSwitch.")

    # Zustand eines Items aktualisieren
    items_api.update_item_state("testNumber", "42")
    print("State of testNumber updated.")

    # Zustand eines Items abrufen
    test_switch_state = items_api.get_item_state("testSwitch")
    print("testSwitch State:", test_switch_state)

    # Ein Item löschen
    items_api.delete_item("newSwitch")
    print("newSwitch deleted.")

    # Gruppenmitglied hinzufügen
    items_api.add_group_member("Static", "newNumber")
    print("newNumber added to Static group.")

    # Gruppenmitglied entfernen
    items_api.remove_group_member("Static", "newNumber")
    print("newNumber removed from Static group.")
    
    # Metadaten hinzufügen
    metadata = {
        "value": "metadata_value",
        "config": {
            "key1": "value1",
            "key2": "value2"
        }
    }
    items_api.add_metadata("testSwitch", "exampleNamespace", metadata)
    print("Metadata added to testSwitch.")

    # Metadaten entfernen
    items_api.remove_metadata("testSwitch", "exampleNamespace")
    print("Metadata removed from testSwitch.")

    # Metadaten-Namespaces eines Items abrufen
    metadata_namespaces = items_api.get_metadata_namespaces("testSwitch")
    print("Metadata namespaces for testSwitch:", metadata_namespaces)
    """
    # Item mit semantischer Klasse abrufen
    #semantic_item = items_api.get_semantic_item("testLocation", "Location")
    #print("Semantic item for testLocation:", semantic_item)

    # Einem Item ein Tag hinzufügen
    items_api.add_tag("testSwitch", "NewTag")
    print("Tag added to testSwitch.")

    # Einem Item ein Tag entfernen
    items_api.remove_tag("testSwitch", "NewTag")
    print("Tag removed from testSwitch.")

    # Verwaiste Metadaten löschen
    items_api.purge_orphaned_metadata()
    print("Orphaned metadata purged.")
    """
# Funktion ausführen
if __name__ == "__main__":
    examples()

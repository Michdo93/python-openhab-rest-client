import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Tags

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
tags_api = Tags(client)

# Beispiele für die Tags-API
def tags_examples():
    # Alle Tags abrufen
    all_tags = tags_api.get_tags()
    print("All Tags:", all_tags)

    # Ein neues Tag erstellen
    # Beispiel für das Tag-Datenobjekt
    new_tag_data = {
        "uid": "CustomTag",
        "name": "CustomTag",
        "label": "My Custom Tag",
        "description": "This is a custom tag",
        "synonyms": ["Custom", "Tag"],
        "editable": True
    }

    try:
        response = tags_api.create_tag(new_tag_data)
        print("Tag Created:", response)
    except Exception as e:
        print("Error creating tag:", e)

    # Details zu einem Tag abrufen
    tag_details = tags_api.get_tag("Property_Voltage")
    print("Details for newTag:", tag_details)

    # Ein Tag aktualisieren
    updated_tag_data = {
        "id": "Property_Voltage",
        "label": "Updated Tag"
    }
    tags_api.update_tag("Property_Voltage", new_tag_data)
    print("newTag updated.")

    # Ein Tag löschen
    tags_api.delete_tag("Property_Voltage")
    print("newTag deleted.")

# Funktion ausführen
if __name__ == "__main__":
    tags_examples()
  
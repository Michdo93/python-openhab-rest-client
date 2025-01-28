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
    new_tag_data = {
        "id": "newTag",
        "label": "New Tag",
        "type": "semantic"
    }
    tags_api.create_tag(new_tag_data)
    print("New Tag created.")

    # Details zu einem Tag abrufen
    tag_details = tags_api.get_tag("newTag")
    print("Details for newTag:", tag_details)

    # Ein Tag aktualisieren
    updated_tag_data = {
        "id": "newTag",
        "label": "Updated Tag",
        "type": "semantic"
    }
    tags_api.update_tag("newTag", updated_tag_data)
    print("newTag updated.")

    # Ein Tag löschen
    tags_api.delete_tag("newTag")
    print("newTag deleted.")

# Funktion ausführen
if __name__ == "__main__":
    tags_examples()
  
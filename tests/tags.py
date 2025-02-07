import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Tags

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
tagsApi = Tags(client)

# Beispiele für die Tags-API
def tagsExamples():
    # Alle Tags abrufen
    allTags = tagsApi.getTags()
    print("All Tags:", allTags)

    # Ein neues Tag erstellen
    # Beispiel für das Tag-Datenobjekt
    newTagData = {
        "uid": "CustomTag",
        "name": "CustomTag",
        "label": "My Custom Tag",
        "description": "This is a custom tag",
        "synonyms": ["Custom", "Tag"],
        "editable": True
    }

    try:
        response = tagsApi.createTag(newTagData)
        print("Tag Created:", response)
    except Exception as e:
        print("Error creating tag:", e)

    # Details zu einem Tag abrufen
    tagDetails = tagsApi.getTag("Property_Voltage")
    print("Details for newTag:", tagDetails)

    # Ein Tag aktualisieren
    updatedTagData = {
        "id": "Property_Voltage",
        "label": "Updated Tag"
    }
    tagsApi.updateTag("Property_Voltage", newTagData)
    print("newTag updated.")

    # Ein Tag löschen
    tagsApi.deleteTag("Property_Voltage")
    print("newTag deleted.")

# Funktion ausführen
if __name__ == "__main__":
    tagsExamples()

import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Transformations

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
transformations = Transformations(client)

# Alle Transformationen abrufen
transformations_list = transformations.get_transformations()
print(transformations_list)

# Eine spezifische Transformation abrufen
uid = "your-transformation-uid"
transformation = transformations.get_transformation(uid)
print(transformation)

# Eine Transformation aktualisieren
updated_data = {
    "uid": "your-transformation-uid",
    "label": "Updated Label",
    "type": "new-type",
    "configuration": {
        "additionalProp1": "value1",
        "additionalProp2": "value2"
    },
    "editable": True
}
updated_transformation = transformations.update_transformation(uid, updated_data)
print(updated_transformation)

# Eine Transformation löschen
deleted_transformation = transformations.delete_transformation(uid)
print(deleted_transformation)

# Alle Transformation-Dienste abrufen
services = transformations.get_transformation_services()
print(services)


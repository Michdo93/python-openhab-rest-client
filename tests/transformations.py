import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Transformations

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
transformationsApi = Transformations(client)

# Alle Transformationen abrufen
#transformationsList = transformationsApi.getTransformations()
#print(transformationsList)

# Eine spezifische Transformation abrufen
uid = "en.map"
#transformation = transformationsApi.getTransformation(uid)
#print(transformation)

# Eine Transformation aktualisieren
updatedData = {
    "uid": "my_custom_map",
    "label": "My Custom Map",
    "type": "map",
    "configuration": {"function": "CLOSED=geschlossen\nOPEN=offen\nNULL=unbekannt\n"},
    "editable": True
}
#updatedTransformation = transformationsApi.updateTransformation(uid, updatedData)
#print(updatedTransformation)

# Eine Transformation löschen
deletedTransformation = transformationsApi.deleteTransformation(uid)
print(deletedTransformation)

# Alle Transformation-Dienste abrufen
services = transformationsApi.getTransformationServices()
print(services)

import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ThingTypes

# OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
thingTypesApi = ThingTypes(client)

# Alle Thing-Typen abrufen
try:
    allThingTypes = thingTypesApi.getAllThingTypes()
    print("Alle Thing-Typen:")
    for thingType in allThingTypes:
        print(f"- {thingType['UID']}: {thingType['label']}")
except Exception as e:
    print(f"Fehler beim Abrufen der Thing-Typen: {e}")

# Spezifischen Thing-Typ abrufen
try:
    thingTypeUid = "mqtt:homeassistant"  # Beispiel-UID
    specificThingType = thingTypesApi.getThingType(thingTypeUid)
    print("\nDetails des spezifischen Thing-Typs:")
    print(specificThingType)
except Exception as e:
    print(f"Fehler beim Abrufen des spezifischen Thing-Typs: {e}")

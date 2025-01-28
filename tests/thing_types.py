import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ThingTypes

# OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
thing_types_api = ThingTypes(client)

# Alle Thing-Typen abrufen
try:
    all_thing_types = thing_types_api.get_all_thing_types()
    print("Alle Thing-Typen:")
    for thing_type in all_thing_types:
        print(f"- {thing_type['UID']}: {thing_type['label']}")
except Exception as e:
    print(f"Fehler beim Abrufen der Thing-Typen: {e}")

# Spezifischen Thing-Typ abrufen
try:
    thing_type_uid = "mqtt:homeassistant"  # Beispiel-UID
    specific_thing_type = thing_types_api.get_thing_type(thing_type_uid)
    print("\nDetails des spezifischen Thing-Typs:")
    print(specific_thing_type)
except Exception as e:
    print(f"Fehler beim Abrufen des spezifischen Thing-Typs: {e}")
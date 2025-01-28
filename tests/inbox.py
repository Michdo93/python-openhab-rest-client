import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Inbox

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Inbox-Klasse instanziieren
inbox_api = Inbox(client)

# Alle entdeckten Dinge abrufen
try:
    discovered_things = inbox_api.get_all_discovered_things()
    print("Entdeckte Dinge:", discovered_things)
except Exception as e:
    print("Fehler beim Abrufen der entdeckten Dinge:", e)

# Ein Entdeckungsergebnis entfernen
thing_uid_to_remove = "thingUID123"
try:
    response = inbox_api.remove_discovery_result(thing_uid_to_remove)
    print("Entdeckungsergebnis entfernt:", response)
except Exception as e:
    print("Fehler beim Entfernen des Entdeckungsergebnisses:", e)

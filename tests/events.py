import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Events

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Events-Klasse instanziieren
events_api = Events(client)

# Alle Events abrufen
try:
    events = events_api.get_all_events(topics="topic1,topic2")
    print("Gefilterte Events:", events)
except ValueError as e:
    print("Fehler beim Abrufen der Events:", e)

# Neue Status-Tracker-Verbindung initiieren
try:
    connection_id = events_api.initiate_state_tracker()
    print("Neue Verbindungs-ID:", connection_id)
except Exception as e:
    print("Fehler beim Starten der Status-Tracker-Verbindung:", e)

# Liste von Items für die Verbindung aktualisieren
try:
    result = events_api.update_sse_connection_items(connection_id="12345", items=["item1", "item2"])
    print("Erfolgreich aktualisiert:", result)
except ValueError as e:
    print("Fehler beim Aktualisieren der Verbindung:", e)

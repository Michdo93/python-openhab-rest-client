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
    connection_id_response = events_api.initiate_state_tracker()
    print("Neue Verbindungs-ID:", connection_id_response)
except Exception as e:
    print("Fehler beim Starten der Status-Tracker-Verbindung:", e)

connection_id = None
for line in connection_id_response.iter_lines():
    if line.startswith(b"data: "):  # Die Zeile mit der ID suchen
        connection_id = line.decode().split("data: ")[1].strip()
        break  # Nur die erste "data: ..." Zeile auslesen

print("Gefundene Connection ID:", connection_id)

# Verbindung aktualisieren
try:
    result = events_api.update_sse_connection_items(connection_id=connection_id, items=["item1", "item2"])
    print(result)
except ValueError as e:
    print("Fehler beim Aktualisieren der Verbindung:", e)

import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Events

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Events-Klasse instanziieren
eventsApi = Events(client)

# Alle Events abrufen
try:
    events = eventsApi.getAllEvents(topics="topic1,topic2")
    print("Gefilterte Events:", events)
except ValueError as e:
    print("Fehler beim Abrufen der Events:", e)

# Neue Status-Tracker-Verbindung initiieren
try:
    connectionIdResponse = eventsApi.initiateStateTracker()
    print("Neue Verbindungs-ID:", connectionIdResponse)
except Exception as e:
    print("Fehler beim Starten der Status-Tracker-Verbindung:", e)

connectionId = None
for line in connectionIdResponse.iter_lines():
    if line.startswith(b"data: "):  # Die Zeile mit der ID suchen
        connectionId = line.decode().split("data: ")[1].strip()
        break  # Nur die erste "data: ..." Zeile auslesen

print("Gefundene Connection ID:", connectionId)

# Verbindung aktualisieren
try:
    result = eventsApi.updateSseConnectionItems(connectionId=connectionId, items=["item1", "item2"])
    print(result)
except ValueError as e:
    print("Fehler beim Aktualisieren der Verbindung:", e)

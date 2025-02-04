import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ThingEvents

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
thing_events = ThingEvents(client)

# Beispielaufrufe
print(thing_events.ThingAddedEvent("*"))
print(thing_events.ThingRemovedEvent("*"))
print(thing_events.ThingUpdatedEvent("*"))
print(thing_events.ThingStatusInfoEvent("*"))
print(thing_events.ThingStatusInfoChangedEvent("*"))

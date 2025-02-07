import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ThingEvents

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
thingEvents = ThingEvents(client)

# Beispielaufrufe
print(thingEvents.ThingAddedEvent("*"))
print(thingEvents.ThingRemovedEvent("*"))
print(thingEvents.ThingUpdatedEvent("*"))
print(thingEvents.ThingStatusInfoEvent("*"))
print(thingEvents.ThingStatusInfoChangedEvent("*"))

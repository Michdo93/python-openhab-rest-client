import sys
import os
import json

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ItemEvents

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
itemEvents = ItemEvents(client)

# Beispielaufrufe
print(itemEvents.ItemEvent())
print(itemEvents.ItemAddedEvent("*"))
print(itemEvents.ItemRemovedEvent("*"))
print(itemEvents.ItemUpdatedEvent("*"))
print(itemEvents.ItemCommandEvent("*"))
print(itemEvents.ItemStateEvent("*"))
print(itemEvents.ItemStatePredictedEvent("*"))
print(itemEvents.ItemStateChangedEvent("*"))
print(itemEvents.GroupItemStateChangedEvent("*", "*"))


response =  itemEvents.ItemStateChangedEvent()

with response as events:
    for line in events.iter_lines():
        line = line.decode()

        if "data" in line:
            line = line.replace("data: ", "")

            try:
                data = json.loads(line)
                print(data)
            except json.decoder.JSONDecodeError:
                print("Event could not be converted to JSON")
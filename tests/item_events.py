import sys
import os
import json

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ItemEvents

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
item_events = ItemEvents(client)

# Beispielaufrufe
print(item_events.ItemEvent())
print(item_events.ItemAddedEvent("*"))
print(item_events.ItemRemovedEvent("*"))
print(item_events.ItemUpdatedEvent("*"))
print(item_events.ItemCommandEvent("*"))
print(item_events.ItemStateEvent("*"))
print(item_events.ItemStatePredictedEvent("*"))
print(item_events.ItemStateChangedEvent("*"))
print(item_events.GroupItemStateChangedEvent("*", "*"))


response =  item_events.ItemStateChangedEvent()

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
import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, LinkEvents

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
linkEvents = LinkEvents(client)

# Beispielaufrufe
print(linkEvents.ItemChannelLinkAddedEvent("*", "*"))
print(linkEvents.ItemChannelLinkRemovedEvent("*", "*"))

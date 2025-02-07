import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ConfigDescriptions

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# ConfigDescriptions-Klasse instanziieren
configDescriptionsApi = ConfigDescriptions(client)

# Alle Konfigurationsbeschreibungen abrufen
allConfigs = configDescriptionsApi.getAllConfigDescriptions(language="en")
print("Alle Konfigurationsbeschreibungen:", allConfigs)

# Eine spezifische Konfigurationsbeschreibung nach URI abrufen
try:
    configByUri = configDescriptionsApi.getConfigDescriptionByUri(uri="channel-type:mqtt:ha-channel", language="en")
    print("Konfigurationsbeschreibung für URI:", configByUri)
except ValueError as e:
    print("Fehler:", e)

import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ConfigDescriptions

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# ConfigDescriptions-Klasse instanziieren
config_descriptions_api = ConfigDescriptions(client)

# Alle Konfigurationsbeschreibungen abrufen
all_configs = config_descriptions_api.get_all_config_descriptions(language="en")
print("Alle Konfigurationsbeschreibungen:", all_configs)

# Eine spezifische Konfigurationsbeschreibung nach URI abrufen
try:
    config_by_uri = config_descriptions_api.get_config_description_by_uri(uri="channel-type:mqtt:ha-channel", language="en")
    print("Konfigurationsbeschreibung für URI:", config_by_uri)
except ValueError as e:
    print("Fehler:", e)

import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Links

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Links-Klasse instanziieren
links_api = Links(client)

# Alle Links abrufen
try:
    links = links_api.get_all_links(channel_uid="someChannelUID")
    print("Alle Links:", links)
except Exception as e:
    print("Fehler beim Abrufen der Links:", e)

# Einen einzelnen Link abrufen
item_name = "TemperatureItem"
channel_uid = "someChannelUID"
try:
    link = links_api.get_individual_link(item_name, channel_uid)
    print("Einzelner Link:", link)
except Exception as e:
    print("Fehler beim Abrufen des Links:", e)

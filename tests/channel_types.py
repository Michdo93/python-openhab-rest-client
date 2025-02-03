import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ChannelTypes

# Beispiel: OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# ChannelTypes-Klasse instanziieren
channel_types_api = ChannelTypes(client)

all_channel_types = channel_types_api.get_all_channel_types(language="en")
print("Alle verfügbaren Channel-Typen:")
for channel in all_channel_types:
    print(channel.get("UID", "Kein UID gefunden"))

# Alle Channel-Typen abrufen
#all_channel_types = channel_types_api.get_all_channel_types(language="en", prefixes="mqtt")
#print("Alle Channel-Typen:", all_channel_types)

# Einen spezifischen Channel-Typ nach UID abrufen
channel_type_details = channel_types_api.get_channel_type_by_uid(channel_type_uid="mqtt:trigger", language="en")
print("Channel-Typ-Details:", channel_type_details)

# Linkbare Item-Typen für einen Channel-Typ abrufen
linkable_item_types = channel_types_api.get_linkable_item_types(channel_type_uid="mqtt:trigger")
print("Linkbare Item-Typen:", linkable_item_types)

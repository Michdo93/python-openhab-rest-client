import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ChannelTypes

# Beispiel: OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# ChannelTypes-Klasse instanziieren
channelTypesApi = ChannelTypes(client)

allChannelTypes = channelTypesApi.getAllChannelTypes(language="en")
print("Alle verfügbaren Channel-Typen:")
for channel in allChannelTypes:
    print(channel.get("UID", "Kein UID gefunden"))

# Alle Channel-Typen abrufen
allChannelTypes = channelTypesApi.getAllChannelTypes(language="en", prefixes="mqtt")
print("Alle Channel-Typen:", allChannelTypes)

# Einen spezifischen Channel-Typ nach UID abrufen
channelTypeDetails = channelTypesApi.getChannelTypeByUid(channelTypeUid="mqtt:trigger", language="en")
print("Channel-Typ-Details:", channelTypeDetails)

# Linkbare Item-Typen für einen Channel-Typ abrufen
linkableItemTypes = channelTypesApi.getLinkableItemTypes(channelTypeUid="mqtt:trigger")
print("Linkbare Item-Typen:", linkableItemTypes)

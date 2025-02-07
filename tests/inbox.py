import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Inbox

# OpenHAB-Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Inbox-API instanziieren
inboxApi = Inbox(client)

# 1. Alle entdeckten Dinge abrufen
try:
    discoveredThings = inboxApi.getAllDiscoveredThings()
    print("Entdeckte Dinge:", discoveredThings)
except Exception as e:
    print("Fehler beim Abrufen der entdeckten Dinge:", e)

# 2. Ein Entdeckungsergebnis entfernen
thingUidToRemove = "avmfritz:fritzbox:192_168_3_1"
try:
    response = inboxApi.removeDiscoveryResult(thingUidToRemove)
    print(f"Entdeckungsergebnis '{thingUidToRemove}' entfernt:", response)
except Exception as e:
    print(f"Fehler beim Entfernen des Entdeckungsergebnisses '{thingUidToRemove}':", e)

# 3. Ein Gerät genehmigen
thingUidToApprove = "avmfritz:fritzbox:192_168_2_1"
thingLabel = "Mein FritzBox Router"
try:
    response = inboxApi.approveDiscoveryResult(thingUidToApprove, thingLabel)
    print(f"Entdeckungsergebnis '{thingUidToApprove}' genehmigt:", response)
except Exception as e:
    print(f"Fehler beim Genehmigen des Entdeckungsergebnisses '{thingUidToApprove}':", e)

# 4. Ein Entdeckungsergebnis ignorieren
thingUidToIgnore = "avmfritz:fritzbox:192_168_2_1"
try:
    response = inboxApi.ignoreDiscoveryResult(thingUidToIgnore)
    print(f"Entdeckungsergebnis '{thingUidToIgnore}' ignoriert:", response)
except Exception as e:
    print(f"Fehler beim Ignorieren des Entdeckungsergebnisses '{thingUidToIgnore}':", e)

# 5. Ein ignoriertes Gerät wieder sichtbar machen
thingUidToUnignore = "avmfritz:fritzbox:192_168_2_1"
try:
    response = inboxApi.unignoreDiscoveryResult(thingUidToUnignore)
    print(f"Entdeckungsergebnis '{thingUidToUnignore}' wieder aktiviert:", response)
except Exception as e:
    print(f"Fehler beim Wiederherstellen des Entdeckungsergebnisses '{thingUidToUnignore}':", e)


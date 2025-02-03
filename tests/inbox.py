import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Inbox

# OpenHAB-Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Inbox-API instanziieren
inbox_api = Inbox(client)

# 1. Alle entdeckten Dinge abrufen
"""
try:
    discovered_things = inbox_api.get_all_discovered_things()
    print("Entdeckte Dinge:", discovered_things)
except Exception as e:
    print("Fehler beim Abrufen der entdeckten Dinge:", e)

# 2. Ein Entdeckungsergebnis entfernen
thing_uid_to_remove = "avmfritz:fritzbox:192_168_3_1"
try:
    response = inbox_api.remove_discovery_result(thing_uid_to_remove)
    print(f"Entdeckungsergebnis '{thing_uid_to_remove}' entfernt:", response)
except Exception as e:
    print(f"Fehler beim Entfernen des Entdeckungsergebnisses '{thing_uid_to_remove}':", e)
"""
# 3. Ein Gerät genehmigen
thing_uid_to_approve = "avmfritz:fritzbox:192_168_2_1"
thing_label = "Mein FritzBox Router"
try:
    response = inbox_api.approve_discovery_result(thing_uid_to_approve, thing_label)
    print(f"Entdeckungsergebnis '{thing_uid_to_approve}' genehmigt:", response)
except Exception as e:
    print(f"Fehler beim Genehmigen des Entdeckungsergebnisses '{thing_uid_to_approve}':", e)
"""
# 4. Ein Entdeckungsergebnis ignorieren
thing_uid_to_ignore = "avmfritz:fritzbox:192_168_2_1"
try:
    response = inbox_api.ignore_discovery_result(thing_uid_to_ignore)
    print(f"Entdeckungsergebnis '{thing_uid_to_ignore}' ignoriert:", response)
except Exception as e:
    print(f"Fehler beim Ignorieren des Entdeckungsergebnisses '{thing_uid_to_ignore}':", e)

# 5. Ein ignoriertes Gerät wieder sichtbar machen
thing_uid_to_unignore = "avmfritz:fritzbox:192_168_2_1"
try:
    response = inbox_api.unignore_discovery_result(thing_uid_to_unignore)
    print(f"Entdeckungsergebnis '{thing_uid_to_unignore}' wieder aktiviert:", response)
except Exception as e:
    print(f"Fehler beim Wiederherstellen des Entdeckungsergebnisses '{thing_uid_to_unignore}':", e)
"""
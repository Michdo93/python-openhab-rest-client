import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Discovery

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Discovery-Klasse instanziieren
discoveryApi = Discovery(client)

# Alle Bindings abrufen, die Discovery unterstützen
bindings = discoveryApi.getAllDiscoveryBindings()
print("Bindings mit Discovery-Funktion:", bindings)

# Einen Discovery-Scan für ein bestimmtes Binding starten
try:
    timeout = discoveryApi.startBindingScan(bindingID="some-binding-id")
    print(f"Discovery gestartet. Timeout: {timeout} Sekunden")
except ValueError as e:
    print("Fehler:", e)

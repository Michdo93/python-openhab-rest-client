import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Audio

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
audioApi = Audio(client)

# Teste Audio-Endpunkte
print(audioApi.getDefaultSink())
print(audioApi.getDefaultSource())
print(audioApi.getSinks())
print(audioApi.getSources())

import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, UUID

# Client initialisieren (ersetze 'http://openhab-url' mit deiner URL und 'auth_token' mit deinem Token)
# client = OpenHABClient(base_url='http://openhab-url', auth_token='your_auth_token')
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
uuidApi = UUID(client)

# Rufe die UUID ab
try:
    openhabUuid = uuidApi.getUUID()
    print(f"Die UUID von OpenHAB ist: {openhabUuid}")
except Exception as e:
    print(f"Fehler beim Abrufen der UUID: {e}")

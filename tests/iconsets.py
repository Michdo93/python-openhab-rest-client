import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Iconsets

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Iconsets-Klasse instanziieren
iconsetsApi = Iconsets(client)

# Alle Iconsets abrufen
try:
    iconsets = iconsetsApi.getAllIconsets(language="de")
    print("Verfügbare Iconsets:", iconsets)
except Exception as e:
    print("Fehler beim Abrufen der Iconsets:", e)

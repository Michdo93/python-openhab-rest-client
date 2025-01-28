import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Templates

# OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
templates_api = Templates(client)

# Alle Templates abrufen
try:
    all_templates = templates_api.get_all_templates()
    print("Alle Templates:")
    for template in all_templates:
        print(f"- {template['uid']}: {template['label']}")
except Exception as e:
    print(f"Fehler beim Abrufen der Templates: {e}")

# Spezifisches Template abrufen
try:
    template_uid = "example_template_uid"  # Beispiel-UID
    specific_template = templates_api.get_template_by_uid(template_uid)
    print("\nDetails des spezifischen Templates:")
    print(specific_template)
except Exception as e:
    print(f"Fehler beim Abrufen des spezifischen Templates: {e}")

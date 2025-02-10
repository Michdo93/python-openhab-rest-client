import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Templates

# OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
templatesApi = Templates(client)

# Alle Templates abrufen
try:
    allTemplates = templatesApi.getAllTemplates()
    print("Alle Templates:")
    for template in allTemplates:
        print(f"- {template['uid']}: {template['label']}")
except Exception as e:
    print(f"Fehler beim Abrufen der Templates: {e}")

# Spezifisches Template abrufen
try:
    templateUid = "example_template_uid"  # Beispiel-UID
    specificTemplate = templatesApi.getTemplateByUID(templateUid)
    print("\nDetails des spezifischen Templates:")
    print(specificTemplate)
except Exception as e:
    print(f"Fehler beim Abrufen des spezifischen Templates: {e}")

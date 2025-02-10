import sys
import os
from datetime import datetime
import pytz

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Actions

# Client initialisieren (ersetze 'http://openhab-url' mit deiner URL und 'auth_token' mit deinem Token)
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
actionsApi = Actions(client)

# Alle Aktionen für ein Thing abrufen
thingUid = "astro:sun:560560e11a"  # Beispiel-Thing UID
try:
    actions = actionsApi.getAllActions(thingUid)
    print("Verfügbare Aktionen:")
    for action in actions:
        print(f"Aktion UID: {action['actionUid']}, Label: {action['label']}")
except Exception as e:
    print(f"Fehler beim Abrufen der Aktionen: {e}")

# Eine Aktion ausführen
actionUid = "astro.getEventTime"  # Beispiel-Aktions-UID

# Eingabedaten vorbereiten (wir wählen den Phase "SUNSET" als Beispiel)
phaseName = "SUN_SET"  # Korrekt geschriebener Phase Name (z. B. "SUNRISE", "SUNSET", "NOON")
momentValue = "START"  # Standardwert für "moment" ist "START"

# Aktuelles Datum und Uhrzeit im ISO 8601-Format mit Zeitzone (ZonedDateTime)
# Hier wird ein korrekt formatierter "ZonedDateTime"-String erzeugt
now = datetime.now(pytz.utc)
dateValueZoned = now.strftime('%Y-%m-%dT%H:%M:%S%z')  # Format: "2025-01-27T14:30:00+00:00"

# Hier wird ein Beispiel für die Eingabedaten vorbereitet
actionInputs = {
    "phaseName": phaseName,  # Phase Name ist erforderlich
    "date": str(dateValueZoned),  # Datum im korrekten ZonedDateTime-Format
    "moment": momentValue    # Moment (START oder END)
}

try:
    # Eine Aktion ausführen
    response = actionsApi.executeAction(thingUid, actionUid, actionInputs)
    print(f"Aktionsantwort: {response}")
    
    # Antwort prüfen
    if isinstance(response, dict):
        print(f"Antwort von der Aktion: {response}")
    else:
        print(f"Unerwarteter Rückgabetyp: {type(response)}")
    
except Exception as e:
    print(f"Fehler beim Ausführen der Aktion: {e}")

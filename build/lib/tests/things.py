import sys
import os
import time
import traceback

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Things

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
thingsApi = Things(client)


def safeCall(description, func, *args, **kwargs):
    try:
        print(f"{description}...")
        response = func(*args, **kwargs)
        print("Erfolgreich:", response)
    except Exception as e:
        print(f"Fehler bei {description}: {e}")
        traceback.print_exc()  # Stacktrace ausgeben

# 1. Alle Things abrufen
#safeCall("Alle Things abrufen", thingsApi.getAllThings)

# 2. Ein spezifisches Thing per UID abrufen
thingUID = "mqtt:topic:mybroker:newthing"
safeCall(f"Thing {thingUID} abrufen", thingsApi.getThingByUID, thingUID)

# 3. Ein neues Thing erstellen
newThing = {
    "UID": "mqtt:topic:mybroker:newthing",
    "label": "Neues MQTT Thing",
    "thingTypeUID": "mqtt:topic",
    "bridgeUID": "mqtt:broker:mybroker",
    "configuration": {},
    "channels": []
}
safeCall("Neues Thing erstellen", thingsApi.createThing, newThing)

#time.sleep(2)  # Warte, damit OpenHAB das neue Thing registrieren kann

thingUID = "mqtt:topic:mybroker:newthing"
# 4. Ein Thing aktualisieren
updatedData = {"label": "Aktualisiertes MQTT Thing"}
#safeCall(f"Thing {thingUID} aktualisieren", thingsApi.updateThing, thingUID, updatedData)

# 5. Ein Thing löschen
#safeCall(f"Thing {thingUID} löschen", thingsApi.deleteThing, thingUID, force=True)

# 6. Die Konfiguration eines Things aktualisieren
configUpdate = {"retain": True}
safeCall(f"Thing {thingUID} Konfiguration aktualisieren", thingsApi.updateThingConfiguration, thingUID, configUpdate)

# 7. Den Status eines Things abrufen
#safeCall(f"Thing {thingUID} Status abrufen", thingsApi.getThingStatus, thingUID)

# 8. Ein Thing aktivieren oder deaktivieren
safeCall(f"Thing {thingUID} aktivieren", thingsApi.enableThing, thingUID, enabled=True)

# 9. Den Firmware-Status abrufen
safeCall(f"Thing {thingUID} Firmware-Status abrufen", thingsApi.getThingFirmwareStatus, thingUID)

# 10. Eine Firmware aktualisieren
firmwareVersion = "1.2.3"
safeCall(f"Thing {thingUID} Firmware auf {firmwareVersion} aktualisieren", thingsApi.updateThingFirmware, thingUID, firmwareVersion)

# 11. Alle verfügbaren Firmwares für ein Thing abrufen
safeCall(f"Thing {thingUID} verfügbare Firmwares abrufen", thingsApi.getThingFirmwares, thingUID)

# 12. Den Konfigurationsstatus eines Things abrufen
safeCall(f"Thing {thingUID} Konfigurationsstatus abrufen", thingsApi.getThingConfigStatus, thingUID)

print("Alle API-Tests abgeschlossen.")

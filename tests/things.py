import sys
import os
import time
import traceback

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Things

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
things_api = Things(client)


def safe_call(description, func, *args, **kwargs):
    try:
        print(f"{description}...")
        response = func(*args, **kwargs)
        print("Erfolgreich:", response)
    except Exception as e:
        print(f"Fehler bei {description}: {e}")
        traceback.print_exc()  # Stacktrace ausgeben

# 1. Alle Things abrufen
#safe_call("Alle Things abrufen", things_api.get_all_things)

# 2. Ein spezifisches Thing per UID abrufen
thing_uid = "mqtt:topic:mybroker:newthing"
safe_call(f"Thing {thing_uid} abrufen", things_api.get_thing_by_uid, thing_uid)

# 3. Ein neues Thing erstellen
new_thing = {
    "UID": "mqtt:topic:mybroker:newthing",
    "label": "Neues MQTT Thing",
    "thingTypeUID": "mqtt:topic",
    "bridgeUID": "mqtt:broker:mybroker",
    "configuration": {},
    "channels": []
}
#safe_call("Neues Thing erstellen", things_api.create_thing, new_thing)

#time.sleep(2)  # Warte, damit OpenHAB das neue Thing registrieren kann

thing_uid = "mqtt:topic:mybroker:newthing"
# 4. Ein Thing aktualisieren
updated_data = {"label": "Aktualisiertes MQTT Thing"}
#safe_call(f"Thing {thing_uid} aktualisieren", things_api.update_thing, thing_uid, updated_data)

# 5. Ein Thing löschen
#safe_call(f"Thing {thing_uid} löschen", things_api.delete_thing, thing_uid, force=True)

# 6. Die Konfiguration eines Things aktualisieren
config_update = {"retain": True}
safe_call(f"Thing {thing_uid} Konfiguration aktualisieren", things_api.update_thing_configuration, thing_uid, config_update)

# 7. Den Status eines Things abrufen
#safe_call(f"Thing {thing_uid} Status abrufen", things_api.get_thing_status, thing_uid)

# 8. Ein Thing aktivieren oder deaktivieren
safe_call(f"Thing {thing_uid} aktivieren", things_api.enable_thing, thing_uid, enabled=True)

# 9. Den Firmware-Status abrufen
safe_call(f"Thing {thing_uid} Firmware-Status abrufen", things_api.get_thing_firmware_status, thing_uid)

# 10. Eine Firmware aktualisieren
firmware_version = "1.2.3"
safe_call(f"Thing {thing_uid} Firmware auf {firmware_version} aktualisieren", things_api.update_thing_firmware, thing_uid, firmware_version)

# 11. Alle verfügbaren Firmwares für ein Thing abrufen
safe_call(f"Thing {thing_uid} verfügbare Firmwares abrufen", things_api.get_thing_firmwares, thing_uid)

# 12. Den Konfigurationsstatus eines Things abrufen
safe_call(f"Thing {thing_uid} Konfigurationsstatus abrufen", things_api.get_thing_config_status, thing_uid)

print("Alle API-Tests abgeschlossen.")

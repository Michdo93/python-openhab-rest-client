import sys
import os
from openhab import OpenHABClient, Things

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
things_api = Things(client)

# Beispielmethoden für die Things-API

def example_get_all_things():
    """Beispiel: Alle Things abrufen."""
    all_things = things_api.get_all_things(summary=True)  # Beispiel mit Zusammenfassung
    print("All Things (Summary):", all_things)

    # Alle Things mit statischen Daten abrufen
    static_things = things_api.get_all_things(static_data_only=True)
    print("All Things (Static Data Only):", static_things)

def example_create_thing():
    """Beispiel: Ein neues Thing erstellen."""
    thing_data = {
        "uid": "newThingUID",
        "label": "New Thing",
        "thingTypeUID": "someThingType",
        "location": "Living Room"
    }
    response = things_api.create_thing(thing_data)
    print("Created Thing Response:", response)

def example_get_thing_by_uid():
    """Beispiel: Details zu einem Thing anhand der UID abrufen."""
    thing_uid = "someThingUID"
    thing_details = things_api.get_thing_by_uid(thing_uid)
    print(f"Details of {thing_uid}:", thing_details)

def example_update_thing():
    """Beispiel: Ein Thing anhand der UID aktualisieren."""
    thing_uid = "someThingUID"
    updated_data = {
        "label": "Updated Thing",
        "location": "Bedroom"
    }
    response = things_api.update_thing(thing_uid, updated_data)
    print(f"Updated {thing_uid}:", response)

def example_delete_thing():
    """Beispiel: Ein Thing löschen."""
    thing_uid = "someThingUID"
    response = things_api.delete_thing(thing_uid)
    print(f"Deleted {thing_uid}:", response)

def example_update_thing_configuration():
    """Beispiel: Die Konfiguration eines Things aktualisieren."""
    thing_uid = "someThingUID"
    new_config = {
        "configuration": {
            "parameter1": "value1",
            "parameter2": "value2"
        }
    }
    response = things_api.update_thing_configuration(thing_uid, new_config)
    print(f"Updated Configuration of {thing_uid}:", response)

def example_enable_thing():
    """Beispiel: Ein Thing aktivieren/deaktivieren."""
    thing_uid = "someThingUID"
    response = things_api.enable_thing(thing_uid, enabled=True)
    print(f"Enabled {thing_uid}:", response)

    response = things_api.enable_thing(thing_uid, enabled=False)
    print(f"Disabled {thing_uid}:", response)

def example_get_thing_status():
    """Beispiel: Den Status eines Things abfragen."""
    thing_uid = "someThingUID"
    status = things_api.get_thing_status(thing_uid)
    print(f"Status of {thing_uid}:", status)

def example_get_thing_firmware_status():
    """Beispiel: Den Firmware-Status eines Things abfragen."""
    thing_uid = "someThingUID"
    firmware_status = things_api.get_thing_firmware_status(thing_uid)
    print(f"Firmware Status of {thing_uid}:", firmware_status)

def example_update_thing_firmware():
    """Beispiel: Die Firmware eines Things aktualisieren."""
    thing_uid = "someThingUID"
    firmware_version = "1.0.1"
    response = things_api.update_thing_firmware(thing_uid, firmware_version)
    print(f"Updated Firmware of {thing_uid} to version {firmware_version}:", response)

def example_get_thing_firmwares():
    """Beispiel: Alle verfügbaren Firmwares für ein Thing abrufen."""
    thing_uid = "someThingUID"
    firmwares = things_api.get_thing_firmwares(thing_uid)
    print(f"Available Firmwares for {thing_uid}:", firmwares)

def example_get_thing_config_status():
    """Beispiel: Den Konfigurationsstatus eines Things abfragen."""
    thing_uid = "someThingUID"
    config_status = things_api.get_thing_config_status(thing_uid)
    print(f"Config Status of {thing_uid}:", config_status)

# Hauptfunktion, die alle Beispielmethoden ausführt
def things_examples():
    # 1. Alle Things abrufen
    example_get_all_things()

    # 2. Ein neues Thing erstellen
    example_create_thing()

    # 3. Details zu einem Thing abrufen
    example_get_thing_by_uid()

    # 4. Ein Thing aktualisieren
    example_update_thing()

    # 5. Ein Thing löschen
    example_delete_thing()

    # 6. Die Konfiguration eines Things aktualisieren
    example_update_thing_configuration()

    # 7. Den Status eines Things ändern (aktivieren/deaktivieren)
    example_enable_thing()

    # 8. Den Status eines Things abfragen
    example_get_thing_status()

    # 9. Den Firmware-Status eines Things abfragen
    example_get_thing_firmware_status()

    # 10. Die Firmware eines Things aktualisieren
    example_update_thing_firmware()

    # 11. Alle verfügbaren Firmwares für ein Thing abrufen
    example_get_thing_firmwares()

    # 12. Den Konfigurationsstatus eines Things abfragen
    example_get_thing_config_status()

# Funktion ausführen
if __name__ == "__main__":
    things_examples()

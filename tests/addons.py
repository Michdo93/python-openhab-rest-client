import sys
import os
import json

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Addons

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
addons_api = Addons(client)

# Teste den Endpunkt, um alle Add-ons zu holen
def test_get_addons():
    print("Teste get_addons...")
    response = addons_api.get_addons()
    print("Antwort von get_addons:", json.dumps(response, indent=2))

# Teste den Endpunkt, um ein spezifisches Add-on zu holen
def test_get_addon():
    addon_id = "binding-astro"  # Beispiel Addon-ID, ändern je nach Bedarf
    print(f"Teste get_addon für ID {addon_id}...")
    response = addons_api.get_addon(addon_id)
    print(f"Antwort von get_addon für {addon_id}:", json.dumps(response, indent=2))

# Teste den Endpunkt, um ein Add-on zu installieren
def test_install_addon():
    addon_id = "binding-astro"  # Beispiel Addon-ID, ändern je nach Bedarf
    print(f"Teste install_addon für ID {addon_id}...")
    response = addons_api.install_addon(addon_id)
    print(f"Antwort von install_addon für {addon_id}:", json.dumps(response, indent=2))

# Teste den Endpunkt, um ein Add-on zu deinstallieren
def test_uninstall_addon():
    addon_id = "binding-astro"  # Beispiel Addon-ID, ändern je nach Bedarf
    print(f"Teste uninstall_addon für ID {addon_id}...")
    response = addons_api.uninstall_addon(addon_id)
    print(f"Antwort von uninstall_addon für {addon_id}:", json.dumps(response, indent=2))

# Teste den Endpunkt, um Add-on-Typen zu holen
def test_get_addon_types():
    print("Teste get_addon_types...")
    response = addons_api.get_addon_types()
    print("Antwort von get_addon_types:", json.dumps(response, indent=2))

# Teste den Endpunkt, um empfohlene Add-ons zu holen
def test_get_addon_suggestions():
    print("Teste get_addon_suggestions...")
    response = addons_api.get_addon_suggestions()
    print("Antwort von get_addon_suggestions:", json.dumps(response, indent=2))

if __name__ == "__main__":
    # Führe alle Tests aus
    #test_get_addons()
    test_get_addon()
    test_install_addon()
    test_uninstall_addon()
    test_get_addon_types()
    test_get_addon_suggestions()

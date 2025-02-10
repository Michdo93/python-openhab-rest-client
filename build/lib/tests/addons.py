import sys
import os
import json

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Addons

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
addonsApi = Addons(client)

# Teste den Endpunkt, um alle Add-ons zu holen
def testGetAddons():
    print("Teste getAddons...")
    response = addonsApi.getAddons()
    print("Antwort von getAddons:", json.dumps(response, indent=2))

# Teste den Endpunkt, um ein spezifisches Add-on zu holen
def testGetAddon():
    addonId = "binding-astro"
    print(f"Teste getAddon für ID {addonId}...")
    response = addonsApi.getAddon(addonId)
    print(f"Antwort von getAddon für {addonId}:", json.dumps(response, indent=2))

# Teste den Endpunkt, um ein Add-on zu installieren
def testInstallAddon():
    addonId = "binding-astro"
    print(f"Teste installAddon für ID {addonId}...")
    response = addonsApi.installAddon(addonId)
    print(f"Antwort von installAddon für {addonId}:", json.dumps(response, indent=2))

# Teste den Endpunkt, um ein Add-on zu deinstallieren
def testUninstallAddon():
    addonId = "binding-astro"
    print(f"Teste uninstallAddon für ID {addonId}...")
    response = addonsApi.uninstallAddon(addonId)
    print(f"Antwort von uninstallAddon für {addonId}:", json.dumps(response, indent=2))

# Teste den Endpunkt, um Add-on-Typen zu holen
def testGetAddonTypes():
    print("Teste getAddonTypes...")
    response = addonsApi.getAddonTypes()
    print("Antwort von getAddonTypes:", json.dumps(response, indent=2))

# Teste den Endpunkt, um empfohlene Add-ons zu holen
def testGetAddonSuggestions():
    print("Teste getAddonSuggestions...")
    response = addonsApi.getAddonSuggestions()
    print("Antwort von getAddonSuggestions:", json.dumps(response, indent=2))

# Teste den Endpunkt, um die Add-on-Konfiguration zu holen
def testGetAddonConfig():
    addonId = "binding-astro"
    print(f"Teste getAddonConfig für ID {addonId}...")
    response = addonsApi.getAddonConfig(addonId)
    print(f"Antwort von getAddonConfig für {addonId}:", json.dumps(response, indent=2))

# Teste den Endpunkt, um die Add-on-Konfiguration zu aktualisieren
def testUpdateAddonConfig():
    addonId = "binding-astro"  # OpenHAB Binding für Sonnen- und Mondzeiten
    configData = {
        "latitude": 52.52,  # Berlin
        "longitude": 13.405, 
        "interval": 300  # Aktualisierung alle 5 Minuten
    }
    print(f"Teste updateAddonConfig für ID {addonId} mit {configData}...")
    response = addonsApi.updateAddonConfig(addonId, configData)
    print(f"Antwort von updateAddonConfig für {addonId}:", json.dumps(response, indent=2))

# Teste den Endpunkt, um Add-on-Services zu holen
def testGetAddonServices():
    print("Teste getAddonServices...")
    response = addonsApi.getAddonServices()
    print("Antwort von getAddonServices:", json.dumps(response, indent=2))

def testInstallAddonFromUrl():
    # Ersetze diese URL durch eine echte OpenHAB-Add-on-URL
    url = "https://repo1.maven.org/maven2/org/smarthomej/addons/bundles/org.smarthomej.binding.amazonechocontrol/4.2.0/org.smarthomej.binding.amazonechocontrol-4.2.0.kar"
    
    print(f"Teste installAddonFromUrl für URL {url}...")
    response = addonsApi.installAddonFromUrl(url)
    print(f"Antwort von installAddonFromUrl für URL {url}:", json.dumps(response, indent=2))

if __name__ == "__main__":
    # Führe alle Tests aus
    testGetAddons()
    testGetAddon()
    testInstallAddon()
    testUninstallAddon()
    testGetAddonTypes()
    testGetAddonSuggestions()
    testGetAddonConfig()
    testUpdateAddonConfig()
    testGetAddonServices()
    testInstallAddonFromUrl()

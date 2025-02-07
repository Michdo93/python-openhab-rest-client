import sys
import os
import json
import time

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Links

# OpenHAB-Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Links-Klasse instanziieren
linksApi = Links(client)

# Test-Daten (basierend auf deiner Liste)
testLinks = [
    {"itemName": "Sunrise_Time", "channelUID": "astro:sun:home:rise#start"},
    {"itemName": "Sunset_Time", "channelUID": "astro:sun:home:set#start"},
    {"itemName": "Azimuth", "channelUID": "astro:sun:home:position#azimuth"},
    {"itemName": "Elevation", "channelUID": "astro:sun:home:position#elevation"},
    {"itemName": "Moon_Phase", "channelUID": "astro:moon:home:phase#name"},
    {"itemName": "Moon_Azimuth", "channelUID": "astro:moon:home:position#azimuth"},
    {"itemName": "Moon_Elevation", "channelUID": "astro:moon:home:position#elevation"},
]

try:
    print("\n**1. Alle Links abrufen**")
    allLinks = linksApi.getAllLinks()
    print(json.dumps(allLinks, indent=2))
    
    itemName = "Sunrise_Time2"
    channelUid = "astro:sun:home:rise#start"

    print(f"\n**2. Einzelnen Link abrufen: {itemName} -> {channelUid}**")
    try:
        singleLink = linksApi.getIndividualLink(itemName, channelUid)
        print(json.dumps(singleLink, indent=2))
    except Exception as e:
        print(f"Fehler: {e}")

    print(f"\n**3. Lösche den Link: {itemName} -> {channelUid}**")
    try:
        unlinkResponse = linksApi.unlinkItemFromChannel(itemName, channelUid)
        print(f"Link entfernt: {unlinkResponse}")
        time.sleep(1)  # Kleine Pause für API-Stabilität
    except Exception as e:
        print(f"Fehler: {e}")

    print(f"\n**4. Verknüpfe Item erneut: {itemName} -> {channelUid}**")
    try:
        config = {}  # Falls Konfiguration notwendig ist, hier ergänzen
        linkResponse = linksApi.linkItemToChannel(itemName, channelUid, config)
        print(f"Link erstellt: {json.dumps(linkResponse, indent=2)}")
    except Exception as e:
        print(f"Fehler: {e}")
    
    print("\n**5. Orphan-Links abrufen**")
    try:
        orphanLinks = linksApi.getOrphanLinks()
        print(json.dumps(orphanLinks, indent=2))
    except Exception as e:
        print(f"Fehler bei Orphan-Links: {e}")

    print("\n**6. Unbenutzte Links bereinigen**")
    try:
        purgeResponse = linksApi.purgeUnusedLinks()
        print(f"Unbenutzte Links bereinigt: {purgeResponse}")
    except Exception as e:
        print(f"Fehler: {e}")

except Exception as e:
    print(f"**Gesamtfehler:** {e}")

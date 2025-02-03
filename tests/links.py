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
links_api = Links(client)

# Test-Daten (basierend auf deiner Liste)
test_links = [
    {"itemName": "Sunrise_Time", "channelUID": "astro:sun:home:rise#start"},
    {"itemName": "Sunset_Time", "channelUID": "astro:sun:home:set#start"},
    {"itemName": "Azimuth", "channelUID": "astro:sun:home:position#azimuth"},
    {"itemName": "Elevation", "channelUID": "astro:sun:home:position#elevation"},
    {"itemName": "Moon_Phase", "channelUID": "astro:moon:home:phase#name"},
    {"itemName": "Moon_Azimuth", "channelUID": "astro:moon:home:position#azimuth"},
    {"itemName": "Moon_Elevation", "channelUID": "astro:moon:home:position#elevation"},
]

try:
    #print("\n**1. Alle Links abrufen**")
    #all_links = links_api.get_all_links()
    #print(json.dumps(all_links, indent=2))
    
    item_name = "Sunrise_Time2"
    channel_uid = "astro:sun:home:rise#start"

    print(f"\n**2. Einzelnen Link abrufen: {item_name} -> {channel_uid}**")
    try:
        single_link = links_api.get_individual_link(item_name, channel_uid)
        print(json.dumps(single_link, indent=2))
    except Exception as e:
        print(f"Fehler: {e}")

    print(f"\n**3. Lösche den Link: {item_name} -> {channel_uid}**")
    try:
        unlink_response = links_api.unlink_item_from_channel(item_name, channel_uid)
        print(f"Link entfernt: {unlink_response}")
        time.sleep(1)  # Kleine Pause für API-Stabilität
    except Exception as e:
        print(f"Fehler: {e}")

    print(f"\n**4. Verknüpfe Item erneut: {item_name} -> {channel_uid}**")
    try:
        config = {}  # Falls Konfiguration notwendig ist, hier ergänzen
        link_response = links_api.link_item_to_channel(item_name, channel_uid, config)
        print(f"Link erstellt: {json.dumps(link_response, indent=2)}")
    except Exception as e:
        print(f"Fehler: {e}")
    
    #print("\n**5. Orphan-Links abrufen**")
    #try:
    #    orphan_links = links_api.get_orphan_links()
    #    print(json.dumps(orphan_links, indent=2))
    #except Exception as e:
    #    print(f"Fehler bei Orphan-Links: {e}")

    #print("\n**6. Unbenutzte Links bereinigen**")
    #try:
    #    purge_response = links_api.purge_unused_links()
    #    print(f"Unbenutzte Links bereinigt: {purge_response}")
    #except Exception as e:
    #    print(f"Fehler: {e}")

except Exception as e:
    print(f"**Gesamtfehler:** {e}")

import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Sitemaps

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
sitemaps_api = Sitemaps(client)

# Beispiele für die Sitemaps-API
def sitemaps_examples():
    # 1. Alle Sitemaps abrufen
    try:
        all_sitemaps = sitemaps_api.get_sitemaps()
        print("All Sitemaps:", all_sitemaps)
    except Exception as e:
        print("Error fetching all sitemaps:", e)

    # 2. Details zu einer bestimmten Sitemap abrufen (z.B. 'Sitemap')
    try:
        test_sitemap = sitemaps_api.get_sitemap("Sitemap")
        print("Sitemap Details:", test_sitemap)
    except Exception as e:
        print("Error fetching Sitemap details:", e)

    # 3. Eine bestimmte Seite einer Sitemap abrufen
    try:
        sitemap_page = sitemaps_api.get_sitemap_page("astro", "astro")
        print("Sitemap Page Details:", sitemap_page)
    except Exception as e:
        print("Error fetching sitemap page:", e)

    # 4. Alle Daten einer ganzen Sitemap abrufen
    try:
        full_sitemap = sitemaps_api.get_full_sitemap("astro")
        print("Full Sitemap Details:", full_sitemap)
    except Exception as e:
        print("Error fetching full sitemap:", e)

    # 5. Ereignisse für eine Sitemap abrufen
    try:
        sitemap_events = sitemaps_api.get_sitemap_events("013328fd-d3fd-4de4-8f7d-efe01bad7eac", sitemap="Sitemap")
        print("Sitemap Events:", sitemap_events)
    except Exception as e:
        print("Error fetching sitemap events:", e)

    # 6. Ereignisse für die gesamte Sitemap abrufen
    try:
        full_sitemap_events = sitemaps_api.get_full_sitemap_events("013328fd-d3fd-4de4-8f7d-efe01bad7eac", sitemap="Sitemap")
        print("Full Sitemap Events:", full_sitemap_events)
    except Exception as e:
        print("Error fetching full sitemap events:", e)

    # 7. Eine Subscription für Sitemap-Ereignisse erstellen
    try:
        subscribe_response = sitemaps_api.subscribe_to_sitemap_events()
        print("Subscription Response:", subscribe_response)
    except Exception as e:
        print("Error subscribing to sitemap events:", e)

# Funktion ausführen
if __name__ == "__main__":
    sitemaps_examples()

import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Sitemaps

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
sitemapsApi = Sitemaps(client)

# Beispiele für die Sitemaps-API
def sitemapsExamples():
    # 1. Alle Sitemaps abrufen
    try:
        allSitemaps = sitemapsApi.getSitemaps()
        print("All Sitemaps:", allSitemaps)
    except Exception as e:
        print("Error fetching all sitemaps:", e)

    # 2. Details zu einer bestimmten Sitemap abrufen (z.B. 'Sitemap')
    try:
        testSitemap = sitemapsApi.getSitemap("Sitemap")
        print("Sitemap Details:", testSitemap)
    except Exception as e:
        print("Error fetching Sitemap details:", e)

    # 3. Eine bestimmte Seite einer Sitemap abrufen
    try:
        sitemapPage = sitemapsApi.getSitemapPage("astro", "astro")
        print("Sitemap Page Details:", sitemapPage)
    except Exception as e:
        print("Error fetching sitemap page:", e)

    # 4. Alle Daten einer ganzen Sitemap abrufen
    try:
        fullSitemap = sitemapsApi.getFullSitemap("astro")
        print("Full Sitemap Details:", fullSitemap)
    except Exception as e:
        print("Error fetching full sitemap:", e)

    # 5. Ereignisse für eine Sitemap abrufen
    try:
        sitemapEvents = sitemapsApi.getSitemapEvents("013328fd-d3fd-4de4-8f7d-efe01bad7eac", sitemap="Sitemap")
        print("Sitemap Events:", sitemapEvents)
    except Exception as e:
        print("Error fetching sitemap events:", e)

    # 6. Ereignisse für die gesamte Sitemap abrufen
    try:
        fullSitemapEvents = sitemapsApi.getFullSitemapEvents("013328fd-d3fd-4de4-8f7d-efe01bad7eac", sitemap="Sitemap")
        print("Full Sitemap Events:", fullSitemapEvents)
    except Exception as e:
        print("Error fetching full sitemap events:", e)

    # 7. Eine Subscription für Sitemap-Ereignisse erstellen
    try:
        subscribeResponse = sitemapsApi.subscribeToSitemapEvents()
        print("Subscription Response:", subscribeResponse)
    except Exception as e:
        print("Error subscribing to sitemap events:", e)

# Funktion ausführen
if __name__ == "__main__":
    sitemapsExamples()

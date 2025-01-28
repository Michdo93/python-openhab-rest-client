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
    # Alle Sitemaps abrufen
    all_sitemaps = sitemaps_api.get_all_sitemaps()
    print("All Sitemaps:", all_sitemaps)

    # Details zu einer Sitemap abrufen
    test_sitemap = sitemaps_api.get_sitemap("testSitemap")
    print("testSitemap Details:", test_sitemap)

# Funktion ausführen
if __name__ == "__main__":
    sitemaps_examples()

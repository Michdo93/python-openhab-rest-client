import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Sitemaps

def testGetAllSitemaps(sitemapsAPI: Sitemaps):
    """Retrieve all sitemaps"""
    print("\n~~~~ Test #1 getSitemaps() ~~~~\n")

    try:
        sitemaps = sitemapsAPI.getSitemaps()
        print(json.dumps(sitemaps, indent=4))
    except Exception as e:
        print(f"Error retrieving all sitemaps: {e}")

def testGetSitemap(sitemapsAPI: Sitemaps, sitemapName: str):
    """Retrieve a specific sitemap"""
    print("\n~~~~ Test #2 getSitemap(sitemapName) ~~~~\n")

    try:
        sitemap = sitemapsAPI.getSitemap(sitemapName)
        print(json.dumps(sitemap, indent=4))
    except Exception as e:
        print(f"Error retrieving sitemap {sitemapName}: {e}")

def testGetSitemapPage(sitemapsAPI: Sitemaps, sitemapName: str, pageId: str):
    """Retrieve a specific sitemap page"""
    print("\n~~~~ Test #3 getSitemapPage(sitemapName, pageId) ~~~~\n")

    try:
        sitemapPage = sitemapsAPI.getSitemapPage(sitemapName, pageId)
        print(json.dumps(sitemapPage, indent=4))
    except Exception as e:
        print(f"Error retrieving sitemap page {pageId} from {sitemapName}: {e}")

def testGetFullSitemap(sitemapsAPI: Sitemaps, sitemapName: str):
    """Retrieve all data of a sitemap"""
    print("\n~~~~ Test #4 getFullSitemap(sitemapName) ~~~~\n")

    try:
        fullSitemap = sitemapsAPI.getFullSitemap(sitemapName)
        print(json.dumps(fullSitemap, indent=4))
    except Exception as e:
        print(f"Error retrieving full sitemap {sitemapName}: {e}")

def testGetSitemapEvents(sitemapsAPI: Sitemaps, subscriptionId: str, sitemapName: str):
    """Retrieve events for a sitemap"""
    print("\n~~~~ Test #5 getSitemapEvents(subscriptionId, sitemapName) ~~~~\n")

    try:
        sitemapEvents = sitemapsAPI.getSitemapEvents(subscriptionId, sitemap=sitemapName)
        print(json.dumps(sitemapEvents, indent=4))
    except Exception as e:
        print(f"Error retrieving events for sitemap {sitemapName}: {e}")

def testGetFullSitemapEvents(sitemapsAPI: Sitemaps, subscriptionId: str, sitemapName: str):
    """Retrieve events for the entire sitemap"""
    print("\n~~~~ Test #6 getFullSitemapEvents(subscriptionId, sitemapName) ~~~~\n")

    try:
        fullSitemapEvents = sitemapsAPI.getFullSitemapEvents(subscriptionId, sitemap=sitemapName)
        print(json.dumps(fullSitemapEvents, indent=4))
    except Exception as e:
        print(f"Error retrieving full sitemap events for {sitemapName}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    sitemapsAPI = Sitemaps(client)

    # Example sitemap name and subscription ID
    sitemapName = "Sitemap"
    subscriptionId = "013328fd-d3fd-4de4-8f7d-efe01bad7eac"

    # Execute test functions
    testGetAllSitemaps(sitemapsAPI)                                     # Test #1
    testGetSitemap(sitemapsAPI, sitemapName)                            # Test #2
    testGetSitemapPage(sitemapsAPI, "astro", "astro")                   # Test #3
    testGetFullSitemap(sitemapsAPI, "astro")                            # Test #4
    testGetSitemapEvents(sitemapsAPI, subscriptionId, sitemapName)      # Test #5
    testGetFullSitemapEvents(sitemapsAPI, subscriptionId, sitemapName)  # Test #6

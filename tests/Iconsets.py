import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Iconsets

# Test retrieving all Iconsets
def testGetAllIconsets(iconsetsAPI: Iconsets, language: str = None):
    print("\n~~~~ Test #1: getAllIconsets() ~~~~\n")

    try:
        iconsets = iconsetsAPI.getAllIconsets(language)
        print("Available Iconsets:", iconsets)
    except Exception as e:
        print("Error retrieving Iconsets:", e)

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    iconsetsAPI = Iconsets(client)

    # Variables
    language = "de"

    # Run all tests
    testGetAllIconsets(iconsetsAPI, language)   # Test #1
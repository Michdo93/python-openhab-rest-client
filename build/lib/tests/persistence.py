import sys
import os
import json

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Persistence

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Persistence-Klasse instanziieren
persistenceApi = Persistence(client)

# Alle Persistence-Dienste abrufen
try:
    services = persistenceApi.getAllServices()
    print("Alle Persistence-Dienste:", json.dumps(services, indent=4))
except Exception as e:
    print("Fehler beim Abrufen der Persistence-Dienste:", e)

# Konfiguration eines bestimmten Persistence-Dienstes abrufen
serviceId = "mapdb"
try:
    config = persistenceApi.getServiceConfiguration(serviceId)
    print(f"Konfiguration für {serviceId}:", json.dumps(config, indent=4))
except Exception as e:
    print("Fehler beim Abrufen der Konfiguration:", e)

# Konfiguration eines bestimmten Persistence-Dienstes setzen
newConfig = {"retention": "30d"}
try:
    updatedConfig = persistenceApi.setServiceConfiguration(serviceId, newConfig)
    print(f"Aktualisierte Konfiguration für {serviceId}:", json.dumps(updatedConfig, indent=4))
except Exception as e:
    print("Fehler beim Setzen der Konfiguration:", e)

# Konfiguration eines bestimmten Persistence-Dienstes löschen
try:
    deleteResponse = persistenceApi.deleteServiceConfiguration(serviceId)
    print(f"Konfiguration für {serviceId} gelöscht:", json.dumps(deleteResponse, indent=4))
except Exception as e:
    print("Fehler beim Löschen der Konfiguration:", e)

# Items für einen Persistence-Dienst abrufen
try:
    items = persistenceApi.getItemsForService(serviceId)
    print(f"Items für den Dienst {serviceId}:", json.dumps(items, indent=4))
except Exception as e:
    print("Fehler beim Abrufen der Items:", e)

# Persistence-Daten für ein Item abrufen
itemName = "TemperatureSensor1"
startTime = "2025-01-01T00:00:00.000Z"
endTime = "2025-01-31T23:59:59.999Z"
try:
    itemData = persistenceApi.getItemPersistenceData(serviceId, itemName, startTime=startTime, endTime=endTime)
    print(f"Persistence-Daten für {itemName}:", json.dumps(itemData, indent=4))
except Exception as e:
    print("Fehler beim Abrufen der Persistence-Daten für Item:", e)

# Persistence-Daten für ein Item speichern
time = "2025-01-27T15:30:00.000Z"  # Zeit im richtigen Format
state = "22.5"  # Beispiel für den Zustand des Items
try:
    response = persistenceApi.storeItemData(serviceId, itemName, time, state)
    print("Daten erfolgreich gespeichert:", response)
except Exception as e:
    print("Fehler beim Speichern der Daten:", e)

# Persistence-Daten für ein Item löschen
startTimeDelete = "2025-01-01T00:00:00.000Z"
endTimeDelete = "2025-01-31T23:59:59.999Z"
try:
    deleteItemResponse = persistenceApi.deleteItemData(serviceId, itemName, startTimeDelete, endTimeDelete)
    print(f"Persistence-Daten für {itemName} gelöscht:", json.dumps(deleteItemResponse, indent=4))
except Exception as e:
    print("Fehler beim Löschen der Persistence-Daten für Item:", e)

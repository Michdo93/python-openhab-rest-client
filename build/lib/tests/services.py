import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Services

def main():
    # OpenHAB-Client initialisieren
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

    serviceId = "org.openhab.i18n"
    
    # Services-API-Objekt erstellen
    servicesApi = Services(client)

    # 1. Alle Services abrufen
    print("Alle Services:")
    allServices = servicesApi.getServices(language="de")
    print(allServices)

    # 2. Einzelnen Service abrufen
    print("Einzelner Service:")
    singleService = servicesApi.getService(serviceId)
    print(singleService)
    
    # 3. Konfiguration eines spezifischen Services abrufen
    print(f"\nKonfiguration für den Service {serviceId}:")
    serviceConfig = servicesApi.getServiceConfig(serviceId)
    print(serviceConfig)
    
    # 4. Konfiguration für einen Service aktualisieren
    newConfig = {
        "enabled": True,
        "setting1": "newValue1"
    }
    print(f"\nAktualisierte Konfiguration für {serviceId}:")
    oldConfig = servicesApi.updateServiceConfig(serviceId, newConfig)
    print("Alte Konfiguration:", oldConfig)
    
    # 5. Konfiguration eines Services löschen
    print(f"\nService-Konfiguration für {serviceId} löschen:")
    deletedConfig = servicesApi.deleteServiceConfig(serviceId)
    print("Gelöschte Konfiguration:", deletedConfig)

    # 6. Alle Kontexte eines Services abrufen
    print(f"\nKontexte für {serviceId}:")
    serviceContexts = servicesApi.getServiceContexts(serviceId)
    print(serviceContexts)

if __name__ == "__main__":
    main()

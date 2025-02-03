import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Services

def main():
    # OpenHAB-Client initialisieren
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

    service_id = "org.openhab.i18n"
    
    # Services-API-Objekt erstellen
    services_api = Services(client)

    # 1. Alle Services abrufen
    print("Alle Services:")
    all_services = services_api.get_services(language="de")
    print(all_services)

    # 2. Einzelnen Service abrufen
    print("Einzelner Service:")
    single_service = services_api.get_service(service_id)
    print(single_service)
    
    # 3. Konfiguration eines spezifischen Services abrufen
    print(f"\nKonfiguration für den Service {service_id}:")
    service_config = services_api.get_service_config(service_id)
    print(service_config)
    
    # 4. Konfiguration für einen Service aktualisieren
    new_config = {
        "enabled": True,
        "setting1": "newValue1"
    }
    print(f"\nAktualisierte Konfiguration für {service_id}:")
    old_config = services_api.update_service_config(service_id, new_config)
    print("Alte Konfiguration:", old_config)
    
    # 5. Konfiguration eines Services löschen
    print(f"\nService-Konfiguration für {service_id} löschen:")
    deleted_config = services_api.delete_service_config(service_id)
    print("Gelöschte Konfiguration:", deleted_config)

    # 6. Alle Kontexte eines Services abrufen
    print(f"\nKontexte für {service_id}:")
    service_contexts = services_api.get_service_contexts(service_id)
    print(service_contexts)

if __name__ == "__main__":
    main()

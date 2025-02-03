import sys
import os
import json

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Persistence

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Persistence-Klasse instanziieren
persistence_api = Persistence(client)

# Alle Persistence-Dienste abrufen
#try:
#    services = persistence_api.get_all_services()
#    print("Alle Persistence-Dienste:", json.dumps(services, indent=4))
#except Exception as e:
#    print("Fehler beim Abrufen der Persistence-Dienste:", e)

# Konfiguration eines bestimmten Persistence-Dienstes abrufen
service_id = "mapdb"
#try:
#    config = persistence_api.get_service_configuration(service_id)
#    print(f"Konfiguration für {service_id}:", json.dumps(config, indent=4))
#except Exception as e:
#    print("Fehler beim Abrufen der Konfiguration:", e)

# Konfiguration eines bestimmten Persistence-Dienstes setzen
new_config = {"retention": "30d"}
#try:
#    updated_config = persistence_api.set_service_configuration(service_id, new_config)
#    print(f"Aktualisierte Konfiguration für {service_id}:", json.dumps(updated_config, indent=4))
#except Exception as e:
#    print("Fehler beim Setzen der Konfiguration:", e)

# Konfiguration eines bestimmten Persistence-Dienstes löschen
#try:
#    delete_response = persistence_api.delete_service_configuration(service_id)
#    print(f"Konfiguration für {service_id} gelöscht:", json.dumps(delete_response, indent=4))
#except Exception as e:
#    print("Fehler beim Löschen der Konfiguration:", e)

# Items für einen Persistence-Dienst abrufen
#try:
#    items = persistence_api.get_items_for_service(service_id)
#    print(f"Items für den Dienst {service_id}:", json.dumps(items, indent=4))
#except Exception as e:
#    print("Fehler beim Abrufen der Items:", e)

# Persistence-Daten für ein Item abrufen
item_name = "TemperatureSensor1"
start_time = "2025-01-01T00:00:00.000Z"
end_time = "2025-01-31T23:59:59.999Z"
try:
    item_data = persistence_api.get_item_persistence_data(service_id, item_name, start_time=start_time, end_time=end_time)
    print(f"Persistence-Daten für {item_name}:", json.dumps(item_data, indent=4))
except Exception as e:
    print("Fehler beim Abrufen der Persistence-Daten für Item:", e)

# Persistence-Daten für ein Item speichern
time = "2025-01-27T15:30:00.000Z"  # Zeit im richtigen Format
state = "22.5"  # Beispiel für den Zustand des Items
try:
    response = persistence_api.store_item_data(service_id, item_name, time, state)
    print("Daten erfolgreich gespeichert:", response)
except Exception as e:
    print("Fehler beim Speichern der Daten:", e)

# Persistence-Daten für ein Item löschen
start_time_delete = "2025-01-01T00:00:00.000Z"
end_time_delete = "2025-01-31T23:59:59.999Z"
try:
    delete_item_response = persistence_api.delete_item_data(service_id, item_name, start_time_delete, end_time_delete)
    print(f"Persistence-Daten für {item_name} gelöscht:", json.dumps(delete_item_response, indent=4))
except Exception as e:
    print("Fehler beim Löschen der Persistence-Daten für Item:", e)

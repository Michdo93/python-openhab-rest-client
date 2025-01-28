# OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Persistence-Klasse instanziieren
persistence_api = Persistence(client)

# Alle Persistence-Dienste abrufen
try:
    services = persistence_api.get_all_services()
    print("Alle Persistence-Dienste:", services)
except Exception as e:
    print("Fehler beim Abrufen der Persistence-Dienste:", e)

# Konfiguration eines bestimmten Persistence-Dienstes abrufen
service_id = "mysql"
try:
    config = persistence_api.get_service_configuration(service_id)
    print(f"Konfiguration für {service_id}: {config}")
except Exception as e:
    print("Fehler beim Abrufen der Konfiguration:", e)

# Persistence-Daten für ein Item speichern
item_name = "TemperatureSensor1"
time = "2025-01-27T15:30:00.000Z"
state = "22.5"
try:
    response = persistence_api.store_item_data(service_id, item_name, time, state)
    print("Daten gespeichert:", response)
except Exception as e:
    print("Fehler beim Speichern der Daten:", e)

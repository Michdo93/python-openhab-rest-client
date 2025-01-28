# Beispiel: OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# ConfigDescriptions-Klasse instanziieren
config_descriptions_api = ConfigDescriptions(client)

# Alle Konfigurationsbeschreibungen abrufen
all_configs = config_descriptions_api.get_all_config_descriptions(language="en", scheme="mqtt")
print("Alle Konfigurationsbeschreibungen:", all_configs)

# Eine spezifische Konfigurationsbeschreibung nach URI abrufen
try:
    config_by_uri = config_descriptions_api.get_config_description_by_uri(uri="some-uri", language="en")
    print("Konfigurationsbeschreibung für URI:", config_by_uri)
except ValueError as e:
    print("Fehler:", e)

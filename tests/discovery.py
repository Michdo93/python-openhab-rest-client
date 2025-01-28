# Beispiel: OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Discovery-Klasse instanziieren
discovery_api = Discovery(client)

# Alle Bindings abrufen, die Discovery unterstützen
bindings = discovery_api.get_all_discovery_bindings()
print("Bindings mit Discovery-Funktion:", bindings)

# Einen Discovery-Scan für ein bestimmtes Binding starten
try:
    timeout = discovery_api.start_binding_scan(binding_id="some-binding-id")
    print(f"Discovery gestartet. Timeout: {timeout} Sekunden")
except ValueError as e:
    print("Fehler:", e)

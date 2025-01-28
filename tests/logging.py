# OpenHABClient initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Logging-Klasse instanziieren
logging_api = Logging(client)

# Alle Loggers abrufen
try:
    loggers = logging_api.get_all_loggers()
    print("Alle Loggers:", loggers)
except Exception as e:
    print("Fehler beim Abrufen der Loggers:", e)

# Einen einzelnen Logger abrufen
logger_name = "org.openhab"
try:
    logger = logging_api.get_single_logger(logger_name)
    print(f"Logger {logger_name}:", logger)
except Exception as e:
    print("Fehler beim Abrufen des Loggers:", e)

# Logger modifizieren oder hinzufügen
logger_name = "org.openhab"
level = "DEBUG"
try:
    response = logging_api.modify_or_add_logger(logger_name, level)
    print(f"Logger {logger_name} modifiziert:", response)
except Exception as e:
    print("Fehler beim Modifizieren des Loggers:", e)

# Logger entfernen
try:
    response = logging_api.remove_logger(logger_name)
    print(f"Logger {logger_name} entfernt:", response)
except Exception as e:
    print("Fehler beim Entfernen des Loggers:", e)

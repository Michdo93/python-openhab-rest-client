import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Logging

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")

# Logging-Klasse instanziieren
loggingApi = Logging(client)

# Alle Loggers abrufen
try:
    loggers = loggingApi.getAllLoggers()
    print("Alle Loggers:", loggers)
except Exception as e:
    print("Fehler beim Abrufen der Loggers:", e)

# Einen einzelnen Logger abrufen
loggerName = "org.openhab"
try:
    logger = loggingApi.getSingleLogger(loggerName)
    print(f"Logger {loggerName}:", logger)
except Exception as e:
    print("Fehler beim Abrufen des Loggers:", e)

# Logger modifizieren oder hinzufügen
loggerName = "org.openhab"
level = "DEBUG"
try:
    response = loggingApi.modifyOrAddLogger(loggerName, level)
    print(f"Logger {loggerName} modifiziert:", response)
except Exception as e:
    print("Fehler beim Modifizieren des Loggers:", e)

# Logger entfernen
try:
    response = loggingApi.removeLogger(loggerName)
    print(f"Logger {loggerName} entfernt:", response)
except Exception as e:
    print("Fehler beim Entfernen des Loggers:", e)

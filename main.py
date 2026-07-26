# Hauptdatei zum Starten der Anwendung (Entry Point)

import os
from repository import StudiumRepository
from service import StudiumService
from controller import DashboardController

if __name__ == "__main__":
    # Initialisierung der Architektur-Schichten
    repo = StudiumRepository()
    service = StudiumService(repo)
    controller = DashboardController(service)
    
    # Prüfen, ob die JSON-Dateien bereits existieren; falls nicht, initialisieren
    if not os.path.exists("studium_info.json"):
        controller.initialisiere_json_dateien()
        
    # Starten des Dashboards
    controller.zeige_dashboard()
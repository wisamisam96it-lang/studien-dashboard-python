# Modul für die Geschäftslogik (Service Layer)

from repository import StudiumRepository

class StudiumService:
    """Enthält die Geschäftslogik für Berechnungen und Datenmanipulation."""
    def __init__(self, repository: StudiumRepository):
        self.repository = repository

    def update_stats(self):
        """Aktualisiert automatisch Notendurchschnitt und ECTS basierend auf den Modulen."""
        d = self.repository.load_data()
        if not d:
            return
        
        total_grade, grade_count, total_modules_done = 0.0, 0, 0
        for sem in d.get("studium", {}).get("semester_plan", []):
            for mod in sem.get("module", []):
                note = mod.get("Note")
                if note and str(note).strip() not in ["0.0", "0", "noch nicht erkannt", ""]:
                    try:
                        total_grade += float(note)
                        grade_count += 1
                        total_modules_done += 1
                    except (ValueError, TypeError):
                        continue
                        
        summary = d["studium"]["Prüfungsleistung"].setdefault("wochen_summary", {})
        summary["notendurchschnitt"] = round(total_grade / grade_count, 2) if grade_count > 0 else 0
        summary["gesamt_ects"] = f"{total_modules_done * 5}/180"
        
        self.repository.save_data(d)

    def add_modul(self, semester_name: str, modul_name: str, dozent: str, note: str):
        """Fügt ein neues Modul zum angegebenen Semester hinzu und aktualisiert die Statistiken."""
        d = self.repository.load_data()
        for sem in d.get("studium", {}).get("semester_plan", []):
            if sem["Semester"] == semester_name:
                sem.setdefault("module", []).append({
                    "Modul_Name": modul_name,
                    "Dozent": dozent,
                    "Note": str(note)
                })
                break
        self.repository.save_data(d)
        self.update_stats()

    def update_modul(self, sem_name: str, idx: int, new_name: str, new_doz: str, new_note: str):
        """Aktualisiert die Daten eines bestehenden Moduls."""
        d = self.repository.load_data()
        for sem in d.get("studium", {}).get("semester_plan", []):
            if sem['Semester'] == sem_name:
                sem['module'][idx] = {
                    "Modul_Name": new_name,
                    "Dozent": new_doz,
                    "Note": str(new_note)
                }
                break
        self.repository.save_data(d)
        self.update_stats()

    def delete_modul(self, sem_name: str, idx: int):
        """Löscht ein Modul aus dem entsprechenden Semester."""
        d = self.repository.load_data()
        for sem in d.get("studium", {}).get("semester_plan", []):
            if sem['Semester'] == sem_name:
                del sem['module'][idx]
                break
        self.repository.save_data(d)
        self.update_stats()
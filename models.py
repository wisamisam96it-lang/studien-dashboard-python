# Modul für die Definition der fachlichen Klassen (Domain Model)

class Student:
    """Repräsentiert einen Studenten mit Vor- und Nachnamen."""
    def __init__(self, vorname: str, name: str):
        self.vorname = vorname
        self.name = name

    def to_dict(self) -> dict:
        """Konvertiert das Student-Objekt in ein Dictionary."""
        return {"Name": self.name, "Vorname": self.vorname}


class Modul:
    """Repräsentiert ein einzelnes Modul im Semester."""
    def __init__(self, modul_name: str, dozent: str, note: str):
        self.modul_name = modul_name
        self.dozent = dozent
        self.note = str(note)

    def to_dict(self) -> dict:
        """Konvertiert das Modul-Objekt in ein Dictionary."""
        return {
            "Modul_Name": self.modul_name,
            "Dozent": self.dozent,
            "Note": self.note
        }


class Semester:
    """Repräsentiert ein Semester, das mehrere Module enthält."""
    def __init__(self, semester_name: str, zeitraum: str, ects_punkte: str, anmerkungen: str, module: list = None):
        self.semester_name = semester_name
        self.zeitraum = zeitraum
        self.ects_punkte = ects_punkte
        self.anmerkungen = anmerkungen
        self.module = module if module else []

    def to_dict(self) -> dict:
        """Konvertiert das Semester-Objekt inklusive aller Module in ein Dictionary."""
        return {
            "Semester": self.semester_name,
            "Zeitraum": self.zeitraum,
            "ECTS_Punkte": self.ects_punkte,
            "Anmerkungen": self.anmerkungen,
            "module": [m.to_dict() for m in self.module]
        }


class Pruefgleistung:
    """Repräsentiert die Prüfungsleistung (Leistungsprüfung) am Ende."""
    def __init__(self, total_completed_hours: int, gesamt_ects: str, notendurchschnitt: float, ziel_erreicht: bool, offene_ects: int):
        self.total_completed_hours = total_completed_hours
        self.gesamt_ects = gesamt_ects
        self.notendurchschnitt = notendurchschnitt
        self.ziel_erreicht = ziel_erreicht
        self.offene_ects = offene_ects

    def to_dict(self) -> dict:
        """Konvertiert die Prüfungsleistung in ein Dictionary."""
        return {
            "wochen_summary": {
                "total_completed_hours": self.total_completed_hours,
                "gesamt_ects": self.gesamt_ects,
                "notendurchschnitt": self.notendurchschnitt,
                "ziel_erreicht": self.ziel_erreicht,
                "offene_ects": self.offene_ects
            },
            "wochen_tracker": {"erreichte_stunden": 840, "gesamt_stunden_studium": 4500}
        }


class Studium:
    """Das Hauptmodell: Studium enthält Student, Semester (mit Modulen) und am Ende die Prüfungsleistung."""
    def __init__(self, studiengang: str, regelstudienzeit: str, student: Student, semester_plan: list, pruefgleistung: Pruefgleistung):
        self.studiengang = studiengang
        self.regelstudienzeit = regelstudienzeit
        self.student = student
        self.semester_plan = semester_plan
        self.pruefgleistung = pruefgleistung

    def to_dict(self) -> dict:
        """Konvertiert das gesamte Studium-Objekt in die finale Struktur."""
        return {
            "studium": {
                "Studiengang": self.studiengang,
                "Regelstudienzeit": self.regelstudienzeit,
                "student": self.student.to_dict(),
                "semester_plan": [s.to_dict() for s in self.semester_plan],
                "Prüfungsleistung": self.pruefgleistung.to_dict()
            }
        }
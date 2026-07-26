# Modul für die Benutzeroberfläche und Steuerung (Controller Layer)

from datetime import datetime
from service import StudiumService
from models import Studium, Student, Semester, Modul, Pruefgleistung

class DashboardController:
    """Steuert die Konsolen-Benutzeroberfläche und die Interaktion mit dem Nutzer."""
    def __init__(self, service: StudiumService):
        self.service = service

    def initialisiere_json_dateien(self):
        """Erstellt die JSON-Standarddateien beim ersten Programmstart."""
        student = Student(vorname="Wisam", name="Isam Hussein")
        
        semesters = [
            Semester("1. Semester", "Bis 31.07.2026", "25 ECTS", "Dringend erforderlich", [
                Modul("Medizin für Nichtmediziner:innen I", "Dana M. Simmet", "3"),
                Modul("E-Health", "Jan Rüterbories", "1.7"),
                Modul("Einführung in das wissenschaftliche Arbeiten für IT und Technik", "Markus Kleffmann", "2.7"),
                Modul("Anatomie und Physiologie", "", "2.5")
            ]),
            Semester("2. Semester", "01.08.2026 - 31.01.2027", "0 ECTS", "Ab dem ersten Tag mit 35 Stunden/Woche starten."),
            Semester("3. Semester", "01.02.2027 - 31.07.2027", "0 ECTS", "Im gleichen Lernrhythmus weitermachen."),
            Semester("4. Semester", "01.08.2027 - 31.01.2028", "0 ECTS", "Im gleichen Lernrhythmus weitermachen."),
            Semester("5. Semester", "01.02.2028 - 31.07.2028", "0 ECTS", "Im gleichen Lernrhythmus weitermachen."),
            Semester("6. Semester", "01.08.2028 - 31.01.2029", "0 ECTS", "Letztes Semester – inkl. Bachelorarbeit")
        ]
        
        pruefung = Pruefgleistung(
            total_completed_hours=35,
            gesamt_ects="20/180",
            notendurchschnitt=2.48,
            ziel_erreicht=False,
            offene_ects=160
        )
        
        studium = Studium(
            studiengang="Medizininformatik",
            regelstudienzeit="6 Semestern/ Vollzeit",
            student=student,
            semester_plan=semesters,
            pruefgleistung=pruefung
        )
        
        self.service.repository.save_data(studium.to_dict())

    def hinzufuegen_ui(self):
        """Benutzeroberfläche zum Hinzufügen eines neuen Moduls."""
        print("\n" + "="*50)
        print("NEUES MODUL HINZUFÜGEN")
        print("="*50)
        dropdown_sem = input("Semester wählen (z.B. 1. Semester): ")
        input_modul = input("Modul Name: ")
        input_dozent = input("Dozent: ")
        input_note = input("Note (z.B. 2.48 oder 0.0): ")

        try:
            self.service.add_modul(dropdown_sem, input_modul, input_dozent, input_note)
            print("\n[Erfolg] Modul erfolgreich gespeichert!")
        except Exception as e:
            print(f"\n[Fehler beim Speichern]: {e}")
        
        input("\nDrücke Enter, um zum Dashboard zurückzukehren...")
        self.zeige_dashboard()

    def bearbeiten_ui(self):
        """Benutzeroberfläche zum Bearbeiten oder Löschen vorhandener Module."""
        print("\n" + "="*50)
        print("MODULE BEARBEITEN / LÖSCHEN")
        print("="*50)
        d = self.service.repository.load_data()
        
        modul_options = []
        for sem in d.get("studium", {}).get("semester_plan", []):
            for i, mod in enumerate(sem.get("module", [])):
                print(f"{len(modul_options)+1}. [{sem['Semester']}] {mod.get('Modul_Name', 'Unbekannt')} (Note: {mod.get('Note', '')})")
                modul_options.append((sem['Semester'], i))
                
        if not modul_options:
            print("Keine Module vorhanden.")
            input("\nDrücke Enter, um zurückzukehren...")
            self.zeige_dashboard()
            return

        wahl = input("\nWähle die Nummer des Moduls (oder 'b' für Zurück): ")
        if wahl.lower() == 'b':
            self.zeige_dashboard()
            return
        try:
            idx_opt = int(wahl) - 1
            sem_name, idx = modul_options[idx_opt]
        except (ValueError, IndexError):
            print("Ungültige Auswahl!")
            input("\nDrücke Enter, um fortzufahren...")
            self.bearbeiten_ui()
            return

        aktion = input("Möchtest du das Modul (e)ditieren oder (l)öschen?: ").lower()
        
        try:
            if aktion == 'l':
                self.service.delete_modul(sem_name, idx)
                print("\n[Erfolg] Modul gelöscht.")
            elif aktion == 'e':
                sem_obj = next(s for s in d["studium"]["semester_plan"] if s['Semester'] == sem_name)
                mod = sem_obj['module'][idx]
                new_name = input(f"Name [{mod.get('Modul_Name', '')}]: ") or mod.get('Modul_Name', '')
                new_doz = input(f"Dozent [{mod.get('Dozent', '')}]: ") or mod.get('Dozent', '')
                new_note = input(f"Note [{mod.get('Note', '')}]: ") or mod.get('Note', '')
                
                self.service.update_modul(sem_name, idx, new_name, new_doz, new_note)
                print("\n[Erfolg] Modul aktualisiert.")
        except Exception as e:
            print(f"\n[Fehler]: {e}")
            
        input("\nDrücke Enter, um zum Dashboard zurückzukehren...")
        self.zeige_dashboard()

    def zeige_dashboard(self):
        """Gibt das vollständige Dashboard in der Konsole aus."""
        self.service.update_stats()
        d = self.service.repository.load_data()
            
        data = d.get("studium", {})
        student = data.get("student", {})
        lp = data.get("Prüfungsleistung", {}).get("wochen_summary", {})
        
        ects_str = lp.get('gesamt_ects', '20/180')
        try:
            ects_val = int(ects_str.split('/')[0])
        except (ValueError, TypeError, IndexError):
            ects_val = 20
            
        ects_pct = round((ects_val / 180) * 100, 1)
        
        today = datetime.now()
        start_studium = datetime(2026, 2, 1)
        passed_days = max(0, (today - start_studium).days)
        calculated_stunden = passed_days * 5
        total_stunden = min(5460, calculated_stunden)

        deadlines = [
            ("1. Semester", datetime(2026, 7, 31, 23, 59, 59)),
            ("2. Semester", datetime(2027, 1, 31, 23, 59, 59)), 
            ("3. Semester", datetime(2027, 7, 31, 23, 59, 59)),
            ("4. Semester", datetime(2028, 1, 31, 23, 59, 59)), 
            ("5. Semester", datetime(2028, 7, 31, 23, 59, 59)),
            ("6. Semester", datetime(2029, 1, 31, 23, 59, 59))
        ]
        
        countdown_msg = "Studium abgeschlossen"
        for name, end_date in deadlines:
            if today < end_date:
                diff_delta = end_date - today
                total_days = diff_delta.days
                total_hours = int(diff_delta.total_seconds() // 3600)
                countdown_msg = f"Tage bis Ende {name}: {total_days} Tage (ca. {total_hours} Stunden)"
                break

        max_stunden = 5460
        prozent = round((total_stunden / max_stunden) * 100, 1) if max_stunden > 0 else 0.0

        print("\n" + "="*65)
        print("DASHBOARD")
        print("="*65)
        print(f"Student: {student.get('Vorname', 'Wisam')} {student.get('Name', 'Isam Hussein')}")
        print(f"Studiengang: {data.get('Studiengang', 'Medizininformatik')}")
        print("Studiumregelzeit: Vollzeit / 6. SEMESTERN")
        print(countdown_msg)
        print("-" * 65)
        
        print(f" <= 2.0     35        {str(lp.get('notendurchschnitt', '2.48')): <6}  {str(lp.get('gesamt_ects', '20/180')): <7}")
        print("   ZIEL    SOLL STD   NOTE    ECTS   ")
        
        print(f"\nECTS Fortschritt: {ects_val}/180 ({ects_pct}%)")
        print(f"Gesamtfortschritt: {total_stunden}/{max_stunden} Std. ({prozent}%)")
        print("="*65)
        
        semester_datums = [
            ("01.02.2026", "31.07.2026"),
            ("01.08.2026", "31.01.2027"),
            ("01.02.2027", "31.07.2027"),
            ("01.08.2027", "31.01.2028"),
            ("01.02.2028", "31.07.2028"),
            ("01.08.2028", "31.01.2029")
        ]
        
        print("\nSemester-Plan")
        print("-" * 65)
        for i, sem in enumerate(data.get('semester_plan', [])):
            if i < len(semester_datums):
                start_str, end_str = semester_datums[i]
            else:
                start_str, end_str = ("01.01.2026", "31.12.2026")
                
            start_dt = datetime.strptime(start_str, "%d.%m.%Y")
            end_dt = datetime.strptime(end_str, "%d.%m.%Y")
            rem_days = max(0, (end_dt - today).days)
            
            print(f"\n▼ {sem.get('Semester', f'{i+1}. Semester')} (30 ECTS)")
            print(f"  Start: {start_str} | Ende: {end_str} | Verbleibend: {rem_days} Tage")
            
            modules = sem.get('module', [])
            if modules:
                for m in modules:
                    mod_name = m.get('Mod_Name', m.get('Modul_Name', ''))
                    mod_note = m.get('Note', '')
                    print(f"  {mod_name:<50} {mod_note}")
            else:
                print("  Keine Module eingetragen.")
                
            print("-" * 65)

        print("\nMENÜ:")
        print("1. Modul_Hinzufügen")
        print("2. Modul_Bearbeiten")
        print("3. Beenden")
        print("="*65)
        
        wahl = input("Wähle eine Option (1-3): ")
        if wahl == '1':
            self.hinzufuegen_ui()
        elif wahl == '2':
            self.bearbeiten_ui()
        elif wahl == '3':
            print("Programm beendet.")
        else:
            print("Ungültige Eingabe.")
            self.zeige_dashboard()
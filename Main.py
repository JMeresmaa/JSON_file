import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime, date


class TuntudEesti:
    def __init__(self, master):
        self.master = master
        self.master.title("Tuntud Eesti Inimesed")

        self.load_data()
        self.create_widgets()

    def load_data(self):
        try:
            with open("2018-09-18_tuntud_eesti.json", "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "JSON faili ei leitud!")
            self.master.quit()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "JSON fail ei ole korrektne!")
            self.master.quit()

    def create_widgets(self):
        self.text_box = tk.Text(self.master, wrap='word', height=30, width=80)
        self.text_box.pack(pady=20)
        self.show_data()

    def calculate_age_and_format(self, birth_date):
        today = date.today()
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
        age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
        formatted_birth_date = birth_date_obj.strftime('%d.%m.%Y')
        return age, formatted_birth_date

    def format_death_dates(self, birth_date, death_date):
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").strftime('%d.%m.%Y')
        death_date_obj = datetime.strptime(death_date, "%Y-%m-%d").strftime('%d.%m.%Y')
        return f"{birth_date_obj}-{death_date_obj}"

    def show_data(self):
        total_count = len(self.data)
        longest_name = ""
        oldest_alive = None
        oldest_alive_age = 0
        oldest_dead = None
        oldest_dead_age = 0
        actor_count = 0
        born_in_1997 = 0
        unique_jobs = set()
        more_than_two_names = 0
        same_birth_and_death_day = 0
        alive_count = 0
        dead_count = 0

        for person in self.data:
            name = person.get('nimi', 'N/A')
            birth_date = person.get('sundinud', 'N/A')
            job = person.get('amet', 'N/A')
            death_date = person.get('surnud', 'N/A')

            if len(name) > len(longest_name):
                longest_name = name

            if death_date == '0000-00-00':
                alive_count += 1
                age, formatted_birth_date = self.calculate_age_and_format(birth_date)
                if age > oldest_alive_age:
                    oldest_alive_age = age
                    oldest_alive = f"{name} ({formatted_birth_date})"
            else:
                dead_count += 1
                birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
                death_date_obj = datetime.strptime(death_date, "%Y-%m-%d")
                age = death_date_obj.year - birth_date_obj.year
                formatted_death_dates = self.format_death_dates(birth_date, death_date)
                if age > oldest_dead_age:
                    oldest_dead_age = age
                    oldest_dead = f"{name} ({formatted_death_dates})"

            if "näitleja" in job.lower():
                actor_count += 1

            if birth_date.startswith("1997"):
                born_in_1997 += 1

            unique_jobs.add(job)

            if len(name.split()) > 2:
                more_than_two_names += 1

            if death_date != '0000-00-00' and birth_date[5:] == death_date[5:]:
                same_birth_and_death_day += 1

        results = (
            f"1. Isikute arv kokku: {total_count}\n"
            f"2. Kõige pikem nimi ja tähemärkide arv: {longest_name} ({len(longest_name)})\n"
            f"3. Kõige vanem elav inimene: {oldest_alive} ({oldest_alive_age} aastat)\n"
            f"4. Kõige vanem surnud inimene: {oldest_dead} ({oldest_dead_age} aastat)\n"
            f"5. Näitlejate koguarv: {actor_count}\n"
            f"6. Sündinud 1997 aastal: {born_in_1997}\n"
            f"7. Erinevaid elukutseid: {len(unique_jobs)}\n"
            f"8. Nimi sisaldab rohkem kui kaks nime: {more_than_two_names}\n"
            f"9. Sünniaeg ja surmaaeg on sama v.a. aasta: {same_birth_and_death_day}\n"
            f"10. Elavaid isikuid: {alive_count}\n"
            f"11. Surnud isikuid: {dead_count}\n"
        )

        self.text_box.insert(tk.END, results)
        self.text_box.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = TuntudEesti(root)
    root.mainloop()

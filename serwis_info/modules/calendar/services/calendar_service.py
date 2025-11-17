from datetime import date
import holidays
import json
import os

# Ścieżka do namedays.json - w tym samym folderze co plik serwisu
current_dir = os.path.dirname(os.path.abspath(__file__))
namedays_path = os.path.join(current_dir, "namedays.json")

try:
    with open(namedays_path, "r", encoding="utf-8") as f:
        namedays_data = json.load(f)
except FileNotFoundError:
    print(f"⚠️  Plik {namedays_path} nie został znaleziony!")
    namedays_data = {}

def get_calendar_data():
    """Pobiera dane kalendarza na dzisiejszy dzień"""
    today = date.today()
    day_of_year = today.timetuple().tm_yday

    pl_holidays = holidays.Poland()
    is_holiday = today in pl_holidays
    holiday_name = pl_holidays.get(today) if is_holiday else None

    key = today.strftime("%m-%d")
    namedays = namedays_data.get(key, ["Brak danych"])

    month_names = {
        1: "stycznia", 2: "lutego", 3: "marca", 4: "kwietnia",
        5: "maja", 6: "czerwca", 7: "lipca", 8: "sierpnia", 
        9: "września", 10: "października", 11: "listopada", 12: "grudnia"
    }
    
    formatted_date = f"{today.day} {month_names[today.month]} {today.year}"
    
    return {
        "date": formatted_date,
        "day_of_year": day_of_year,
        "namedays": namedays,
        "is_holiday": is_holiday,
        "holiday_name": holiday_name,
    }
import requests

zodiac_mapping = {
    "baran": "aries",
    "byk": "taurus", 
    "bliznieta": "gemini",
    "rak": "cancer",
    "lew": "leo",
    "panna": "virgo",
    "waga": "libra",
    "skorpion": "scorpio",
    "strzelec": "sagittarius",
    "koziorozec": "capricorn",
    "wodnik": "aquarius",
    "ryby": "pisces"
}

zodiac_polish_names = {
    "baran": "Baran ♈", "byk": "Byk ♉", "bliznieta": "Bliźnięta ♊",
    "rak": "Rak ♋", "lew": "Lew ♌", "panna": "Panna ♍",
    "waga": "Waga ♎", "skorpion": "Skorpion ♏", "strzelec": "Strzelec ♐",
    "koziorozec": "Koziorożec ♑", "wodnik": "Wodnik ♒", "ryby": "Ryby ♓"
}

def translate_to_polish(text: str) -> str:
    """Tłumaczy tekst na polski używając Google Translate API"""
    if not text or text == 'Horoskop niedostępny':
        return text
    
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': 'en', 
            'tl': 'pl',  
            'dt': 't',
            'q': text
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            translated_text = ''.join([item[0] for item in data[0] if item[0]])
            return translated_text
        else:
            print(f"Błąd tłumaczenia: {response.status_code}")
            return text
            
    except Exception as e:
        print(f"Błąd tłumaczenia API: {e}")
        return text

def get_horoscope(zodiac_sign: str):
    """Pobiera horoskop dla danego znaku zodiaku"""
    zodiac_english = zodiac_mapping.get(zodiac_sign.lower())
    if not zodiac_english:
        return {"error": "Nieprawidłowy znak zodiaku"}
    
    try:
        url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={zodiac_english}&day=today"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            api_data = response.json()
            
            if api_data.get('success', False):
                horoscope_data = api_data.get('data', {})
                horoscope_text = horoscope_data.get('horoscope_data', 'Horoskop niedostępny')
                
                translated_horoscope = translate_to_polish(horoscope_text)
                
                return {
                    "zodiac_sign": zodiac_sign,
                    "zodiac_name": zodiac_polish_names[zodiac_sign],
                    "horoscope": translated_horoscope,
                    "date": horoscope_data.get('date', ''),
                    "sign": horoscope_data.get('sign', ''),
                    "success": True
                }
            else:
                return try_second_api(zodiac_english, zodiac_sign)
        else:
            return try_second_api(zodiac_english, zodiac_sign)
            
    except Exception as e:
        return {"error": f"Błąd połączenia z API: {str(e)}"}

def try_second_api(zodiac_english: str, zodiac_sign: str):
    """Spróbuj drugiego API horoskopów"""
    try:
        # Drugie API
        url = f"https://aztro.sameerkumar.website/?sign={zodiac_english}&day=today"
        
        response = requests.post(url, timeout=10)
        
        if response.status_code == 200:
            api_data = response.json()
            
            horoscope_text = api_data.get('description', 'Horoskop niedostępny')
            translated_horoscope = translate_to_polish(horoscope_text)
            
            return {
                "zodiac_sign": zodiac_sign,
                "zodiac_name": zodiac_polish_names[zodiac_sign],
                "horoscope": translated_horoscope,
                "mood": translate_to_polish(api_data.get('mood', '')),
                "compatibility": api_data.get('compatibility', ''),
                "lucky_number": api_data.get('lucky_number', ''),
                "lucky_time": api_data.get('lucky_time', ''),
                "success": True
            }
        else:
            return {"error": f"Oba API zwróciły błąd: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Wszystkie API horoskopów są niedostępne: {str(e)}"}

def get_available_zodiacs():
    """Zwraca listę dostępnych znaków zodiaku"""
    return {
        "available_signs": list(zodiac_mapping.keys()),
        "polish_names": zodiac_polish_names
    }
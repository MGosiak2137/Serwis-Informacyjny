from flask import Blueprint, render_template, request
import requests
import statistics
from datetime import datetime
from googletrans import Translator
from dateutil.parser import isoparse

journey_bp = Blueprint(
    "journey", __name__, url_prefix="/journey", template_folder="../templates", static_folder="../static"
)

API_URL_ROUNDTRIP = "https://priceline-com2.p.rapidapi.com/flights/search-roundtrip"
API_URL_ONEWAY = "https://priceline-com2.p.rapidapi.com/flights/search-one-way"
API_HEADERS = {
    "x-rapidapi-host": "priceline-com2.p.rapidapi.com",
    "x-rapidapi-key": "db58deade0msh6f6f77b75f6a195p12d372jsncb54d5a89da2"
}

API_HOTELS_LOCATIONS = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
API_HOTELS_SEARCH = "https://booking-com.p.rapidapi.com/v1/hotels/search"

BOOKING_HEADERS = {
    "x-rapidapi-host": "booking-com.p.rapidapi.com",
    "x-rapidapi-key": "db58deade0msh6f6f77b75f6a195p12d372jsncb54d5a89da2"
}

translator = Translator()

def translate_to_english(text):
    try:
        translated = translator.translate(text, dest='en')
        return translated.text
    except Exception as e:
        print("Googletrans error:", e)
        return text

def get_booking_dest_id(city_name):
    """Zwraca dest_id z Booking.com API"""
    city_name_en = translate_to_english(city_name)
    params = {
        "name": city_name_en,
        "locale": "en-gb"
    }

    try:
        resp = requests.get(API_HOTELS_LOCATIONS, headers=BOOKING_HEADERS, params=params)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("dest_id")
    except Exception as e:
        print("Booking.com locations API error:", e)

    return None

def fetch_hotels(dest_id, checkin, checkout, adults):
    """Pobiera 5 najtańszych hoteli z Booking.com API"""
    params = {
        "adults_number": adults,
        "room_number": 1,
        "dest_id": dest_id,
        "dest_type": "city",
        "checkin_date": checkin,
        "checkout_date": checkout,
        "locale": "en-gb",
        "filter_by_currency": "USD",
        "order_by": "price",
        "page_number": 0,
        "units": "metric",
        "include_adjacency": "true"
    }

    try:
        resp = requests.get(API_HOTELS_SEARCH, headers=BOOKING_HEADERS, params=params)
        print("Booking API status:", resp.status_code)

        if resp.status_code == 200:
            data = resp.json()
            hotels = data.get("result", [])
            hotels_sorted = sorted(
                hotels,
                key=lambda x: x.get("min_total_price", float("inf"))
            )

            formatted = []
            for h in hotels_sorted[:5]:
                formatted.append({
                    "name": h.get("hotel_name"),
                    "address": h.get("address_trans"),
                    "price_usd": h.get("min_total_price"),
                    "rating": h.get("review_score"),
                    "photo": h.get("max_photo_url")
                })
            return formatted

    except Exception as e:
        print("Booking.com hotels API error:", e)

    return []

def get_iata_code(city_or_airport_name):
    english_name = translate_to_english(city_or_airport_name)
    ac_url = "https://priceline-com2.p.rapidapi.com/flights/auto-complete"
    params = {"query": english_name}
    try:
        response = requests.get(ac_url, headers=API_HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            search_items = data.get("data", {}).get("searchItems", [])
            for item in search_items:
                if item.get("type") == "AIRPORT" and item.get("id"):
                    return item["id"].upper()
    except Exception as e:
        print("Autocomplete API error:", e)
    return city_or_airport_name.strip().upper()[:3]

def safe_parse_iso(datetime_str):
    try:
        return isoparse(datetime_str) if datetime_str else None
    except Exception:
        return None

def parse_segment_times(slice_data):
    if not slice_data or not slice_data.get("segments"):
        return "?", "?", "?", "?", "?", 0
    
    segments = slice_data["segments"]
    dep_seg = segments[0]
    arr_seg = segments[-1]
    
    dep_info = dep_seg.get("departInfo") or {}
    arr_info = arr_seg.get("arrivalInfo") or {}
    
    dep_airport = dep_info.get("airport", {}).get("code", "?")
    arr_airport = arr_info.get("airport", {}).get("code", "?")
    
    dep_time_str = dep_info.get("time", {}).get("dateTime")
    arr_time_str = arr_info.get("time", {}).get("dateTime")

    dep_time = safe_parse_iso(dep_time_str)
    arr_time = safe_parse_iso(arr_time_str)

    duration = "?"
    if dep_time and arr_time:
        td = arr_time - dep_time
        total_seconds = td.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        duration = f"{hours}h {minutes}m"

    dep_time_fmt = dep_time.strftime("%Y-%m-%d %H:%M") if dep_time else "?"
    arr_time_fmt = arr_time.strftime("%Y-%m-%d %H:%M") if arr_time else "?"
    stops = len(segments) - 1
    
    return dep_airport, arr_airport, dep_time_fmt, arr_time_fmt, duration, stops

def fetch_flights_oneway(origin, destination, date, cabin, people):
    params = {
        "originAirportCode": origin,
        "destinationAirportCode": destination,
        "departureDate": date,
        "cabinClass": cabin,
        "passengers": people
    }
    try:
        response = requests.get(API_URL_ONEWAY, headers=API_HEADERS, params=params)
        print(f"DEBUG ONEWAY: {origin}->{destination} status={response.status_code}")
        if response.status_code == 200:
            data = response.json()
            listings = data.get("data", {}).get("listings", [])
            if listings:
                return sorted(listings, key=lambda x: x.get("totalPriceWithDecimal", {}).get("price", float('inf')))
    except Exception as e:
        print("API ERROR:", e)
    return []

@journey_bp.route("/", methods=["GET"])
def journey():
    destination_input = request.args.get("destination", "").strip()
    origin_input = request.args.get("origin", "").strip()
    date_from = request.args.get("date_from", "").strip()
    date_to = request.args.get("date_to", "").strip()
    people_raw = request.args.get("people", "1").strip()
    cabin = request.args.get("cabin", "ECO")

    origin = get_iata_code(origin_input) if origin_input else ""
    destination = get_iata_code(destination_input) if destination_input else ""

    try:
        people = max(1, int(people_raw))
    except:
        people = 1

    flights = []
    avg_price = min_price = max_price = None
    hotels = []

    # USD -> PLN
    try:
        nbp_resp = requests.get("https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json")
        usd_to_pln = nbp_resp.json()["rates"][0]["mid"] if nbp_resp.status_code == 200 else 4.5
    except Exception:
        usd_to_pln = 4.5

    if origin and destination and date_from and date_to:
        # Loty tam
        outbound_flights = fetch_flights_oneway(origin, destination, date_from, cabin, people)
        return_flights = fetch_flights_oneway(destination, origin, date_to, cabin, people)
        prices = []

        if outbound_flights and return_flights:
            max_results = min(5, len(outbound_flights), len(return_flights))
            for i in range(max_results):
                out_flight = outbound_flights[i]
                ret_flight = return_flights[i]

                price_out = out_flight.get("totalPriceWithDecimal", {}).get("price", 0)
                price_ret = ret_flight.get("totalPriceWithDecimal", {}).get("price", 0)
                total_price = price_out + price_ret

                airline_out = out_flight.get("airlines", [{}])[0].get("name", "Nieznana")
                airline_ret = ret_flight.get("airlines", [{}])[0].get("name", "Nieznana")

                out_slices = out_flight.get("slices", [])
                if out_slices:
                    dep_out, arr_out, dep_time_out, arr_time_out, duration_out, stops_out = parse_segment_times(out_slices[0])
                else:
                    dep_out = arr_out = dep_time_out = arr_time_out = duration_out = "?"
                    stops_out = 0

                ret_slices = ret_flight.get("slices", [])
                if ret_slices:
                    dep_ret, arr_ret, dep_time_ret, arr_time_ret, duration_ret, stops_ret = parse_segment_times(ret_slices[0])
                else:
                    dep_ret = arr_ret = dep_time_ret = arr_time_ret = duration_ret = "?"
                    stops_ret = 0

                price_pln = round(total_price * usd_to_pln, 2) if total_price else None
                if total_price:
                    prices.append(total_price)

                flights.append({
                    "airline_out": airline_out,
                    "airline_ret": airline_ret,
                    "price_usd": round(total_price, 2),
                    "price_pln": price_pln,
                    "price_out_usd": round(price_out, 2),
                    "price_ret_usd": round(price_ret, 2),
                    "dep_out": dep_out,
                    "arr_out": arr_out,
                    "dep_time_out": dep_time_out,
                    "arr_time_out": arr_time_out,
                    "duration_out": duration_out,
                    "stops_out": stops_out,
                    "dep_ret": dep_ret,
                    "arr_ret": arr_ret,
                    "dep_time_ret": dep_time_ret,
                    "arr_time_ret": arr_time_ret,
                    "duration_ret": duration_ret,
                    "stops_ret": stops_ret
                })

        if prices:
            avg_price = round(statistics.mean(prices), 2)
            min_price = round(min(prices), 2)
            max_price = round(max(prices), 2)

        # Hotele
        if destination_input and date_from and date_to:
            dest_id = get_booking_dest_id(destination_input)
            if dest_id:
                hotels = fetch_hotels(dest_id, date_from, date_to, adults=people)

    # PODSUMOWANIE LOT + HOTEL
    total_min_flight_usd = min_price if min_price else 0
    try:
        nights = (datetime.strptime(date_to, "%Y-%m-%d") -
                  datetime.strptime(date_from, "%Y-%m-%d")).days
    except:
        nights = 0

    if hotels:
        hotel_usd = hotels[0]["price_usd"]
        hotel_pln = round(hotel_usd * usd_to_pln, 2)
    else:
        hotel_usd = 0
        hotel_pln = 0

    total_usd = round(total_min_flight_usd + hotel_usd * nights, 2)
    total_pln = round(total_usd * usd_to_pln, 2)

    return render_template(
        "journey.html",
        destination=destination_input,
        origin=origin_input,
        date_from=date_from,
        date_to=date_to,
        people=people,
        flights=flights,
        avg_price=avg_price,
        min_price=min_price,
        max_price=max_price,
        cabin=cabin,
        hotels=hotels,
        usd_rate=usd_to_pln,
        nights=nights,
        hotel_usd=hotel_usd,
        hotel_pln=hotel_pln,
        total_usd=total_usd,
        total_pln=total_pln
    )

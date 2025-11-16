from flask import Blueprint, render_template, request
import requests
import statistics

journey_bp = Blueprint(
    "journey", __name__,
    url_prefix="/journey",
    template_folder="../templates",
    static_folder="../static"
)

API_URL = "https://priceline-com2.p.rapidapi.com/flights/search-roundtrip"
API_HEADERS = {
    "x-rapidapi-host": "priceline-com2.p.rapidapi.com",
    "x-rapidapi-key": "db58deade0msh6f6f77b75f6a195p12d372jsncb54d5a89da2"
}


@journey_bp.route("/", methods=["GET"])
def journey():
    destination = request.args.get("destination", "").strip().upper()
    origin = request.args.get("origin", "").strip().upper()
    date_from = request.args.get("date_from", "").strip()
    date_to = request.args.get("date_to", "").strip()
    people_raw = request.args.get("people", "1").strip()
    
    try:
        people = max(1, int(people_raw))
    except:
        people = 1

    flights = []
    avg_price = None
    min_price = None
    max_price = None

    # Jeżeli formularz jest uzupełniony → wołamy API
    if origin and destination and date_from and date_to:
        params = {
            "originAirportCode": origin,
            "destinationAirportCode": destination,
            "departureDate": date_from,
            "returnDate": date_to,
            "cabinClass": "ECO",
            "passengers": people
        }

        try:
            api_response = requests.get(API_URL, headers=API_HEADERS, params=params)
            if api_response.status_code == 200:
                data = api_response.json()
                listings = data.get("data", {}).get("listings", [])

                prices = []

                for flight in listings[:10]:
                    price = flight.get("totalPriceWithDecimal", {}).get("price")
                    airline = flight.get("airlines", [{}])[0].get("name", "Nieznana linia")
                    slices = flight.get("slices", [])
                    
                    if slices:
                        dep = slices[0]["segments"][0]["departInfo"]["airport"]["code"]
                        arr = slices[-1]["segments"][-1]["arrivalInfo"]["airport"]["code"]
                        duration = slices[0]["durationInMinutes"]
                    else:
                        dep = arr = duration = "?"

                    if price:
                        prices.append(price)
                        flights.append({
                            "airline": airline,
                            "dep": dep,
                            "arr": arr,
                            "price": price,
                            "duration": duration
                        })

                if prices:
                    avg_price = round(statistics.mean(prices), 2)
                    min_price = min(prices)
                    max_price = max(prices)

        except Exception as e:
            print("API ERROR:", e)

    return render_template(
        "journey.html",
        destination=destination,
        origin=origin,
        date_from=date_from,
        date_to=date_to,
        people=people,
        flights=flights,
        avg_price=avg_price,
        min_price=min_price,
        max_price=max_price
    )

from flask import Blueprint, render_template, request

journey_bp = Blueprint(
    "journey", __name__,
    template_folder="../../templates" 
)

@journey_bp.route("/journey", methods=["GET"])
def journey():
    destination = request.args.get("destination", "").strip()
    date_from = request.args.get("date_from", "").strip()
    date_to = request.args.get("date_to", "").strip()
    people_raw = request.args.get("people", "1").strip()

    try:
        people = max(1, int(people_raw))
    except (ValueError, TypeError):
        people = 1

    if date_from and date_to and date_from > date_to:
        date_from, date_to = date_to, date_from

    return render_template(
        "journey.html",
        destination=destination or None,
        date_from=date_from or None,
        date_to=date_to or None,
        people=people
    )

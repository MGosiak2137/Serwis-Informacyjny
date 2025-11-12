from flask import Blueprint, render_template

stockmarket_bp = Blueprint("stockmarket", __name__, url_prefix="/stockmarket")

@stockmarket_bp.route("/")
def stockmarket():
    sample_rates = [
        {"name": "WIG20", "code": "W20", "rate": "+0.54%"},
        {"name": "S&P 500", "code": "SPX", "rate": "+0.73%"},
        {"name": "DAX", "code": "DAX", "rate": "-0.12%"},
    ]
    return render_template("stockmarket.html", rates=sample_rates)

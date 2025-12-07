from flask import Blueprint, render_template, request
from flask_login import login_required
import requests

main_eco_bp = Blueprint(
    "main_eco",
    __name__,
    url_prefix="/main_eco",
    template_folder="../templates",
    static_folder="../static"
)

@main_eco_bp.route("/main_eco", methods=["GET"])
@login_required
def main():
    return render_template("nav_foot_eco.html", title="Moduł ekonomiczne")
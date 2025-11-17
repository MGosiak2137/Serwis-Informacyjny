from flask import Blueprint, render_template

main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/main",
    template_folder="../templates",
    static_folder="../static",          
)


@main_bp.route("/",  methods=["GET"])
def index():
    return render_template("index.html", body_class="home-page")

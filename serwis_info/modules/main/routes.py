from flask import Blueprint, render_template

main_bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",         
    static_url_path="/main_static"  
)


@main_bp.route("/")
def index():
    return render_template("index.html", body_class="home-page")

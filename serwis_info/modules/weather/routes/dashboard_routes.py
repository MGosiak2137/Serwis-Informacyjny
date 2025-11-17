from flask import render_template, Blueprint

dashboards_bp = Blueprint(
    "dashboards",
    __name__,
    url_prefix="/dashboards",
    template_folder="../templates",
    static_folder="../static"
)


@dashboards_bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')
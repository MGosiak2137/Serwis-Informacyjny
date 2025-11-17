from flask import render_template

def register_dashboard_routes(bp):

    @bp.route('/')
    @bp.route('/dashboard')
    def dashboard_page():
        return render_template('dashboard.html')

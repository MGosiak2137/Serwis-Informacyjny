from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # importujemy blueprinty (zdefiniowane osobno)
    #from serwis_info.modules.news.routes.news import news_bp
    

    # rejestrujemy blueprinty
    #app.register_blueprint(currencies_bp)
 

    @app.route("/")
    def index():
        return "<h3>Serwis informacyjny — strona główna</h3>"

    return app
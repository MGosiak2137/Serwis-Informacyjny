# Główny plik uruchamiający flaska
# Importuje create_app() z pakietu serwis_info i uruchamia serwer flask

from serwis_info.create_app import create_app
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
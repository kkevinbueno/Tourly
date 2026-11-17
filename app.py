from flask import Flask, jsonify
from flask_cors import CORS
from routes.contato_routes import contato_bp
from routes.reserva_routes import reserva_bp

# static_folder='.' permite servir o front-end também pelo Flask (http://localhost:5000)
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)  # libera o front hospedado no GitHub Pages para chamar esta API

app.register_blueprint(contato_bp, url_prefix="/api/contatos")
app.register_blueprint(reserva_bp, url_prefix="/api/reservas")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

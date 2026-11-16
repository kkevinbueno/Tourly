from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from routes.contato_routes import contato_bp
from routes.config import Config

BASE_DIR = Path(__file__).resolve().parent


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config["JSON_AS_ASCII"] = False
    app.register_blueprint(contato_bp)

    @app.get("/")
    def inicio():
        return send_from_directory(BASE_DIR, "index.html")

    @app.get("/pages/<path:arquivo>")
    def paginas(arquivo):
        return send_from_directory(BASE_DIR / "pages", arquivo)

    @app.get("/css/<path:arquivo>")
    def css(arquivo):
        return send_from_directory(BASE_DIR / "css", arquivo)

    @app.get("/js/<path:arquivo>")
    def javascript(arquivo):
        return send_from_directory(BASE_DIR / "js", arquivo)

    @app.get("/img/<path:arquivo>")
    def imagens(arquivo):
        return send_from_directory(BASE_DIR / "img", arquivo)

    @app.get("/api/health")
    def health():
        status = {"servidor": "online", "banco": "não verificado"}
        try:
            from routes.conexao import Conexao
            con = Conexao().conectar()
            con.close()
            status["banco"] = "conectado"
            return jsonify(status), 200
        except Exception as exc:
            status["banco"] = "desconectado"
            status["detalhe"] = str(exc)
            return jsonify(status), 503

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.DEBUG)

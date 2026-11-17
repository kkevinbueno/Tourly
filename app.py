
from flask import Flask
from routes.contato_routes import contato_bp
from routes.reserva_routes import reserva_bp
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

app.register_blueprint(contato_bp, url_prefix='/api/contatos')
app.register_blueprint(reserva_bp, url_prefix='/api/reservas')

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

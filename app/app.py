from flask import Flask
from flask_cors import CORS

from .config import HOST, PORT, DEBUG, CORS_ORIGINS
from .routes import api


app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)

app.register_blueprint(api)


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)

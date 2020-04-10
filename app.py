import datetime
import json

from flask import Flask, jsonify, render_template
from flask_restplus import Api

from src.view import api as legal_api
from src.redis_client import redis_client


def create_application():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_pyfile('settings.py')
    redis_client.init_app(app)
    api = Api(app)
    api.add_namespace(legal_api)

    @app.route('/index')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    application = create_application()
    application.run(host='localhost', port=5000, debug=True)
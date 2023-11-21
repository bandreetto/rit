from flask import Flask
from .proxy.routes import proxy_blueprint

app = Flask(__name__)

app.register_blueprint(proxy_blueprint)

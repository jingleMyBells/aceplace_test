import logging

from flask import Flask
from flask_mail import Mail
from flask_pymongo import PyMongo

from .settings import Config


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

app = Flask(__name__)
app.config.from_object(Config)
mongodb_client = PyMongo(app, uri=app.config.get('MONGO_INITDB_DATABASE'))
db = mongodb_client.db
mail = Mail(app)

from . import api_views  # noqa

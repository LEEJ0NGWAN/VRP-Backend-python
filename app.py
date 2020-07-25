from flask import Flask
from s3 import app as s3_api

app = Flask(__name__)
app.register_blueprint(s3_api)


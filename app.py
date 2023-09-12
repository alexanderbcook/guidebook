import os
from flask import Flask
from flask import render_template, request, url_for
from pyairtable import Table

app = Flask(__name__)

env_config = os.getenv("PROD_APP_SETTINGS")
app.config.from_object(env_config)

print(env_config)
AIRTABLE_SECRET_TOKEN = os.getenv("AIRTABLE_SECRET_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

TABLE_NAME = "Restaurants"
TABLE = Table(AIRTABLE_SECRET_TOKEN, AIRTABLE_BASE_ID, TABLE_NAME)

@app.route("/")
def hello_world():
    listings = TABLE.all()
    return render_template("base.html", listings=listings)

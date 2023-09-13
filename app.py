import os
from flask import Flask
from flask import render_template, request, url_for
from pyairtable import Table
from collections import OrderedDict

app = Flask(__name__)

env_config = os.getenv("PROD_APP_SETTINGS")
app.config.from_object(env_config)

AIRTABLE_SECRET_TOKEN = os.getenv("AIRTABLE_SECRET_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

TABLE = Table(AIRTABLE_SECRET_TOKEN, AIRTABLE_BASE_ID, "Restaurants")
recommendations = TABLE.all()

@app.route("/")
def return_recommendations():
    neighborhoods   = []
    categories      = []
    cuisines        = []
    cities          = []
    diets           = []

    neighborhoods   = get_data("Neighborhoods"  , neighborhoods)
    categories      = get_data("Categories"     , categories)
    cuisines        = get_data("Cuisines"       , cuisines)
    cities          = get_data("Cities"         , cities)
    diets           = get_data("Special Diets"  , diets)

    swap_ids_to_names(recommendations, neighborhoods,   'Neighborhood')
    swap_ids_to_names(recommendations, categories,      'Categories')
    swap_ids_to_names(recommendations, cuisines,        'Cuisine')
    swap_ids_to_names(recommendations, cities,          'Cities')
    swap_ids_to_names(recommendations, diets,           'Diets')

    return render_template("base.html", recommendations=recommendations, neighborhoods=get_neighborhoods())

def get_data(name, container):
    TABLE = Table(AIRTABLE_SECRET_TOKEN, AIRTABLE_BASE_ID, name)
    container = TABLE.all()

    return container

def swap_ids_to_names(recommendations, records, name):
    for recommendation in recommendations:
        if name in recommendation["fields"].keys():
            for record in records:
                if  recommendation["fields"][name][0] == record["id"]:
                    recommendation["fields"][name][0] =  record["fields"]["Name"]

    return recommendations

def get_neighborhoods():
    all_neighborhoods = [rec["fields"]["Neighborhood"][0] for rec in recommendations if "Neighborhood" in rec["fields"].keys() and len(rec["fields"]["Neighborhood"]) == 1]
    print(all_neighborhoods)
    unique_cats = list(OrderedDict.fromkeys(all_neighborhoods))
    return unique_cats
    #for recommendation in recommendations:
    #    if "Neighborhood" in recommendation["fields"].keys():
    #        print(recommendation["fields"]["Neighborhood"][0])
    
    #unique_neighborhoods = list(OrderedDict.fromkeys(all_cats))
    return 
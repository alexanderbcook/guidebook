import os
from flask import Flask
from flask import render_template, request, url_for
from pyairtable import Table
from pyairtable.formulas import match
from collections import OrderedDict
from flask_assets import Bundle, Environment

app = Flask(__name__)

env_config = os.getenv("PROD_APP_SETTINGS")
app.config.from_object(env_config)

AIRTABLE_SECRET_TOKEN = os.getenv("AIRTABLE_SECRET_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

TABLE = Table(AIRTABLE_SECRET_TOKEN, AIRTABLE_BASE_ID, "Restaurants")
recommendations = TABLE.all()

css_bundle = Bundle('css/global.css',
          'css/nav.css', 
          'css/body.css',
          'css/categories.css',
          'css/footer.css',          
          filters='cssmin', output='css/styles.css')

assets = Environment(app)
assets.register('main_styles', css_bundle)


def get_data(name, container):
    TABLE = Table(AIRTABLE_SECRET_TOKEN, AIRTABLE_BASE_ID, name)
    container = TABLE.all()

    return container

def swap_ids_to_names(recommendations, records, name):
    for recommendation in recommendations:
        if name in recommendation["fields"].keys():
            for record in records:
                i = 0
                while i < len(recommendation["fields"][name]):
                    if  recommendation["fields"][name][i] == record["id"]:
                        recommendation["fields"][name][i] =  record["fields"]["Name"]
                    i+=1


    return recommendations

def get_unique_list(name):
    bulk_list = []
    for recommendation in recommendations:
        if name in recommendation["fields"].keys():
            i = 0
            while i < len(recommendation["fields"][name]):
                if  recommendation["fields"][name][i] not in bulk_list:
                    bulk_list.append(recommendation["fields"][name][i])
                i+=1

    unique_list = list(OrderedDict.fromkeys(bulk_list))
    
    return unique_list

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

@app.route("/")
def return_recommendations():

    return render_template("base.html", recommendations = recommendations,
                                        neighborhoods   = neighborhoods, #get_unique_list("Neighborhood"),
                                        categories      = categories, #get_unique_list("Categories"),
                                        cuisines        = get_unique_list("Cuisine"),
                                        cities          = get_unique_list("Cities"),
                                        diets           = get_unique_list("Diets"))

@app.route("/category/<category>")
def filter_by_category(category):
    filtered_recommendations = []
    
    for recommendation in recommendations:
        if "Categories" in recommendation["fields"].keys():
            if category in recommendation["fields"]["Categories"]:
                filtered_recommendations.append(recommendation)
    
    return render_template("base.html", recommendations = filtered_recommendations, 
                                        categories      = categories, #get_unique_list("Categories"),
                                        cuisines        = get_unique_list("Cuisine"),
                                        cities          = get_unique_list("Cities"),
                                        diets           = get_unique_list("Diets"))

    
from flask import Flask
from flask import render_template, request
from flask_assets import Bundle, Environment
from utilities import   (get_data,
                        swap_ids_to_names,
                        filter_recommendations,
                        fetch_additional_info)

app = Flask(__name__)

css_bundle = Bundle('css/global.css',
          'css/nav.css',
          'css/body.css',
          'css/categories.css',
          'css/about.css',
          filters='cssmin', output='css/styles.css')

assets = Environment(app)
assets.register('main_styles', css_bundle)

recommendations = []
neighborhoods   = []
categories      = []
cuisines        = []
cities          = []
diets           = []

recommendations = get_data("Main List"    , recommendations)
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
    return render_template("base.html",  recommendations = recommendations,
                                         neighborhoods   = neighborhoods,
                                         categories      = categories,
                                         cuisines        = cuisines,
                                         cities          = cities,
                                         diets           = diets)

@app.route("/category/<category>")
def filter_by_category(category):
    filtered_recommendations = []
    filter_recommendations(recommendations, filtered_recommendations, category)
    
    return render_template("body.html",  recommendations = filtered_recommendations,
                                         neighborhoods   = neighborhoods, 
                                         categories      = categories,
                                         cuisines        = cuisines,
                                         cities          = cities,
                                         diets           = diets)

@app.route("/recommendation/<name>")
def return_additional_info(name):
    additional_info = []
    fetch_additional_info(recommendations, additional_info, name)
    
    return render_template("base.html",     recommendations = recommendations,
                                            additional_info = additional_info,
                                            neighborhoods   = neighborhoods,
                                            categories      = categories,
                                            cuisines        = cuisines,
                                            cities          = cities,
                                            diets           = diets)

@app.route("/about/")
def return_about():
    return render_template("about.html")
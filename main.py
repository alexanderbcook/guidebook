from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utilities import   (get_data,
                        swap_ids_to_names,
                        filter_recommendations,
                        fetch_additional_info)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

recommendations = []
neighborhoods   = []
categories      = []
cuisines        = []
cities          = []
diets           = []

recommendations = get_data("Main List"      , recommendations, True)
neighborhoods   = get_data("Neighborhoods"  , neighborhoods, False)
categories      = get_data("Categories"     , categories, False)
cuisines        = get_data("Cuisines"       , cuisines, False)
cities          = get_data("Cities"         , cities, False)
diets           = get_data("Special Diets"  , diets, False)

swap_ids_to_names(recommendations, neighborhoods,   'Neighborhood')
swap_ids_to_names(recommendations, categories,      'Categories')
swap_ids_to_names(recommendations, cuisines,        'Cuisine')
swap_ids_to_names(recommendations, cities,          'Cities')
swap_ids_to_names(recommendations, diets,           'Diets')

@app.get("/", response_class=HTMLResponse)
def return_recommendations(request: Request):
    
    context = {
        "request": request,
        "recommendations": recommendations,
        "neighborhoods": neighborhoods,
        "categories": categories,
        "cuisines": cuisines,
        "cities": cities,
        "diets": diets
    }
    return templates.TemplateResponse("base.html", context)

@app.get("/category/{categoryName}", response_class=HTMLResponse)
def return_filtered_recommendations(request: Request, categoryName: str):

    filtered_recommendations = []
    filter_recommendations(recommendations, filtered_recommendations, categoryName)
    
    context = {
        "request": request,
        "recommendations": filtered_recommendations,
        "neighborhoods": neighborhoods,
        "categories": categories,
        "cuisines": cuisines,
        "cities": cities,
        "diets": diets
    }
    return templates.TemplateResponse("body.html", context)

@app.route("/recommendation/{recommendationName}")
def return_additional_info(request: Request, recommendationName: str):
    additional_info = []
    fetch_additional_info(recommendations, additional_info, recommendationName)
    
    context = {
        "request": request,
        "recommendations": filtered_recommendations,
        "additional_info": additional_info,
        "neighborhoods": neighborhoods,
        "categories": categories,
        "cuisines": cuisines,
        "cities": cities,
        "diets": diets
    }
    return templates.TemplateResponse("body.html", context)

@app.get("/itineraries/", response_class=HTMLResponse)
def return_itineraries(request: Request):

    context = {
        "request": request
    }
    return templates.TemplateResponse("itineraries.html", context)

@app.get("/about/", response_class=HTMLResponse)
def return_about(request:Request):

    context = {
        "request": request
    }

    return templates.TemplateResponse("about.html", context)
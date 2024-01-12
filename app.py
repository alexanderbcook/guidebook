from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utilities import   (get_data,
                        swap_ids_to_names,
                        fetch_filtered_recommendations,
                        fetch_additional_info,
                        fetch_search_results)

app = FastAPI()

origins = ["*"]
app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)

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
        "categories": categories,
    }
    return templates.TemplateResponse("base.html", context)

@app.get("/category/{category_name}", response_class=HTMLResponse)
def return_filtered_recommendations(request: Request, category_name: str):
    filtered_recommendations = []
    fetch_filtered_recommendations(recommendations, filtered_recommendations, category_name)

    context = {
        "request": request,
        "recommendations": filtered_recommendations
    }
    return templates.TemplateResponse("body.html", context)

@app.post("/search/")
async def return_search_results(request: Request):
    search_term = await request.body()

    search_results=[]
    fetch_search_results(recommendations, search_results, search_term)

    context = {
        "request": request,
        "recommendations": search_results
    }
    return templates.TemplateResponse("body.html", context)

@app.get("/recommendation/{recommendation_id}", response_class=HTMLResponse)
def return_additional_info(request: Request, recommendation_id: str):
    additional_info = []
    fetch_additional_info(recommendations, additional_info, recommendation_id)

    context = {
        "request": request,
        "additional_info": additional_info
    }
    return templates.TemplateResponse("modal.html", context)

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

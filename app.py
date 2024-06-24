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


def set_current_view(view):
    global currentView
    currentView = view
    return currentView

def get_current_view():
    global currentView
    return currentView

def set_current_category(category):
    global currentCategory
    currentCategory = category
    return currentCategory

def get_current_category():
    global currentCategory
    return currentCategory

def set_previous_search(results):
    global previousResults
    previousResults = results
    return previousResults

def get_previous_search():
    global previousResults
    return previousResults

def set_search_term(term):
    global searchTerm
    searchTerm = term
    return searchTerm

def get_search_term():
    global searchTerm
    return searchTerm

@app.get("/", response_class=HTMLResponse)
def return_recommendations(request: Request):
    currentView = set_current_view("list")
    curentCategory = set_current_category("List")
    previousResults = set_previous_search(None)
    searchTerm = set_search_term(None)

    context = {
        "request": request,
        "recommendations": recommendations,
        "categories": categories,
        "currentView": currentView,
        "currentCategory": currentCategory
    }
    

    return templates.TemplateResponse("base.html", context)

@app.get('/swapContext/{category_name}', response_class=HTMLResponse)
def swap_context(request: Request, category_name: str):
    currentView = get_current_view()
    currentCategory = set_current_category(category_name)
    searchTerm = get_search_term()

    if(currentCategory in ['Bars', 'Restaurants', 'Activities', 'List']):
        filtered_recommendations = [] 
        data = fetch_filtered_recommendations(recommendations, filtered_recommendations, category_name)
    else:
        data = previousResults

    if currentView == "list":
        currentView = set_current_view("map")
        context = {
            "request": request,
            "recommendations": data,
            "categories": categories,
            "currentCategory": currentCategory,
            "currentView": currentView,
            "searchTerm": searchTerm
        }
        html = "map.html"
        return templates.TemplateResponse(html, context)
    else:
        currentView = set_current_view("list")
        context = {
            "request": request,
            "recommendations": data,
            "categories": categories,
            "currentCategory": currentCategory,
            "currentView": currentView,
            "searchTerm": searchTerm
        }
        html = "body.html"
        return templates.TemplateResponse(html, context)

    
@app.get("/category/{category_name}", response_class=HTMLResponse)
def return_filtered_recommendations(request: Request, category_name: str):
    currentCategory = set_current_category(category_name)
    currentView = get_current_view()
    
    filtered_recommendations = []
    fetch_filtered_recommendations(recommendations, filtered_recommendations, category_name)
    context = {
        "request": request,
        "recommendations": filtered_recommendations,
        "categories": categories,
        "currentView": currentView,
        "currentCategory": currentCategory
    }
    
    if currentView == "list":
        html = "body.html"
    if currentView == "map":
        html = "map.html"
    return templates.TemplateResponse(html, context)

@app.post("/search/")
async def return_search_results(request: Request):
    term = await request.body()
    term = str(term).replace("search_term=","").replace("b'","").replace("'","").lower()
    currentView = set_current_view("list")
    currentCategory = set_current_category("search")
    searchTerm = set_search_term(term)
    previousResults = get_previous_search()

    search_results=[]

    fetch_search_results(recommendations, search_results, term)

    if previousResults is None:
        previousResults = set_previous_search(search_results)

    context = {
        "request": request,
        "recommendations": search_results,
        "categories": categories,
        "currentView": currentView,
        "currentCategory": currentCategory,
        "searchTerm": searchTerm
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

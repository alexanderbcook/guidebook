import os
import time
from collections import OrderedDict
from flask import Flask
from pyairtable import Table

app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS")
app.config.from_object(env_config)

AIRTABLE_SECRET_TOKEN = "patJMTdA6xReF018G.9e1128bbb317fc6263dd7705cc6396d9e218aeae56042807c17b103c48d2f44f"
AIRTABLE_BASE_ID = "app2f7RZsPJOUKXnd"

### Decoraters.

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Calling {func.__name__}.")
        print(f"Execution time: {execution_time} seconds.")
        return result
    return wrapper

### Data layer manipulation utilities.

@timer
def get_data(name, container,sort):
    table = Table(AIRTABLE_SECRET_TOKEN, AIRTABLE_BASE_ID, name)
    if sort:
        container = table.all(sort=["-POTM", "-LastModified"])
    else:
        container = table.all()

    return container

@timer
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

@timer
def get_unique_list(recommendations, name):
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

@timer
def fetch_filtered_recommendations(recommendations, container, category):
    if category == "List":
      for recommendation in recommendations:
        container.append(recommendation)
    else:
        for recommendation in recommendations:
            if "Categories" in recommendation["fields"].keys():
                if category in recommendation["fields"]["Categories"]:
                    container.append(recommendation)

    return container

@timer
def fetch_additional_info(recommendations, container, recommendation_id):
    for recommendation in recommendations:
        if recommendation_id == recommendation["id"]:
            container.append(recommendation)
    return container

@timer
def fetch_search_results(recommendations, container, search_term):
    search_term = str(search_term).replace("search_term=","").replace("b'","").replace("'","").lower()
    for recommendation in recommendations:
        if  search_term in recommendation["fields"]["Name"].lower() and recommendation not in container:
                container.append(recommendation)
        if "Neighborhood" in recommendation["fields"].keys():
            for neighborhood in recommendation["fields"]["Neighborhood"]:
                if search_term in neighborhood.lower() and recommendation not in container:
                    container.append(recommendation)
        if "Tags" in recommendation["fields"].keys():
            for tag in recommendation["fields"]["Tags"]:
                if search_term in tag.lower() and recommendation not in container:
                    container.append(recommendation)
        if "Address" in recommendation["fields"].keys():
            if  search_term in recommendation["fields"]["Address"].lower() and recommendation not in container:
                container.append(recommendation)
    return container


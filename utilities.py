import os
import time
from collections import OrderedDict
from flask import Flask
from pyairtable import Table

app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS")
app.config.from_object(env_config)

AIRTABLE_SECRET_TOKEN = os.getenv("AIRTABLE_SECRET_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

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
        container = table.all(sort=["-LastModified"])
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
def filter_recommendations(recommendations, container, category):
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

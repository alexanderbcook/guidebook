import os
from flask import Flask
from pyairtable import Table
from collections import OrderedDict

app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS")
app.config.from_object(env_config)

AIRTABLE_SECRET_TOKEN = os.getenv("AIRTABLE_SECRET_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

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
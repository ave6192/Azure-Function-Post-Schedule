import datetime
from distutils.command.build_scripts import first_line_re
import logging
from operator import concat, le
import re

import azure.functions as func
import requests


username = "mm_es_masteruser"
password = "PrquqFN<b3aSw4h"

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    entries = getAllDigitalEntries()


    logging.info('Python timer trigger function ran at %s', utc_timestamp)


def getAllDigitalEntries():
    _query = "Digital" 
    first_res = request(0, 20, _query)
    second_res = request(20, first_res[0]-20, _query)

    allEntries = concat(first_res[1], second_res[1])

    return allEntries



def request(_from, _size, _query):
    url = "https://search-mm-dev-ao4q6qdz7r4ovijbe5mlqqdjii.eu-west-2.es.amazonaws.com/liveindexedcontentpageversionviewmodel/_search"
    payload = {"query":{"bool":{"must":[{"term":{"cultureId":127}},{"term":{"pageType":"7"}},{"multi_match":{"query":_query,"type":"phrase","fields":["pageText","keyWords","summaryText","jobSector","title","location","jobRef"]}}]}},"size":_size,"from":_from,"track_scores":"true","sort":["_score"]}

    response = requests.get(url, auth = (username, password), json=payload)
    json = response.json()

    total = getTotal(json)

    logging.info('Response status code is: %s', response.status_code)
    return (total, getEntries(json))



def getTotal(json):
    return json["hits"]["total"]["value"]

def getEntries(json):
    return json["hits"]["hits"]

# 
# def getResults(json):
#     list = json["hits"]["hits"]
#     total = json["hits"]["total"]["value"]
#     for hit in list:
#         print(hit['_source']["title"])






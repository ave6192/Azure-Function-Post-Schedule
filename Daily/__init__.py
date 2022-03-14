import datetime
import logging

import azure.functions as func
import requests

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    json = request()
    getResults(json)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)



def request():
    url = "https://search-mm-dev-ao4q6qdz7r4ovijbe5mlqqdjii.eu-west-2.es.amazonaws.com/liveindexedcontentpageversionviewmodel/_search"
    payload = {"query":{"bool":{"must":[{"term":{"cultureId":127}},{"term":{"pageType":"7"}},{"multi_match":{"query":"Digital","type":"phrase","fields":["pageText","keyWords","summaryText","jobSector","title","location","jobRef"]}}]}},"size":20,"from":0,"track_scores":"true","sort":["_score"]}
    username = "mm_es_masteruser"
    password = "PrquqFN<b3aSw4h"
    #mydata = {'auth': (username, password)}
    response = requests.get(url, auth = (username, password), json=payload)
    logging.info('Response status code is: %s', response.status_code)
    return response.json()


def getResults(json):
    list = json["hits"]["hits"]
    total = json["hits"]["total"]["value"]
    for hit in list:
        print(hit['_source']["title"])






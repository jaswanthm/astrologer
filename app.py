#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "action.yes":
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def makeResult(req):
    #if req.get("contexts").get("name") == "context_name"

    for item in req.get("result").get("contexts"):
        print(item["name"])
        if item["name"] == "context_name":
            resultName = item["parameters"].get("any")

    luckyNumber = "Your lucky number is " + str(numero(resultName))

    return {
        "speech": luckyNumber,
        "displayText": luckyNumber,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-jash"
    }


def numero(myname):
    var = myname
    print(var)
    arr = list(var)
    count = 0
    finalcount = 0
    for a in arr:
        if (a == 'a'):
            count += 1
        elif (a == 'b'):
            count += 2
        elif (a == 'c'):
            count += 3
        elif (a == 'd'):
            count += 4
        elif (a == 'e'):
            count += 5
        elif (a == 'f'):
            count += 8
        elif (a == 'g'):
            count += 3
        elif (a == 'h'):
            count += 5
        elif (a == 'i'):
            count += 1
        elif (a == 'j'):
            count += 1
        elif (a == 'k'):
            count += 2
        elif (a == 'l'):
            count += 3
        elif (a == 'm'):
            count += 4
        elif (a == 'n'):
            count += 5
        elif (a == 'o'):
            count += 7
        elif (a == 'p'):
            count += 8
        elif (a == 'q'):
            count += 1
        elif (a == 'r'):
            count += 2
        elif (a == 's'):
            count += 3
        elif (a == 't'):
            count += 4
        elif (a == 'u'):
            count += 6
        elif (a == 'v'):
            count += 6
        elif (a == 'w'):
            count += 6
        elif (a == 'x'):
            count += 5
        elif (a == 'y'):
            count += 1
        elif (a == 'z'):
            count += 7

    while (count > 0):
        finalcount += (count%10)
        count/=10 

    finalcount = int(finalcount)

    return finalcount


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

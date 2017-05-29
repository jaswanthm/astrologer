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

    luckyNumber = numero(resultName)

    return {
        "speech": luckyNumber,
        "displayText": luckyNumber,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-jash"
    }

def getNumeroText(finalcount):
    if finalcount == 1:
        return "Your lucky number is " + str(finalcount) + " " + " and you are individualistic and independent, showing leadership and drive. The 1 is masculine, focused, an originator and self-starter; it is also progressive, strong-willed, courageous, self-reliant and rebellious (in a constructive way)."
    elif finalcount == 2:
        return "Your lucky number is " + str(finalcount) + " " + " and you are sensitive, tactful, diplomatic and cooperative. The 2s tend to be peacemakers and are loving, studious and patient. A 2 may express many musical or feminine qualities and also tends to be sensual and intuitive."
    elif finalcount == 3:
        return "Your lucky number is " + str(finalcount) + " " + " and you are imaginative, expressive communicators and artists. They are tolerant, joyful, optimistic, inspiring, talented, jovial, youthful, dynamic ... the list goes on and on!"
    elif finalcount == 4:
        return "Your lucky number is " + str(finalcount) + " " + " and you are disciplined, strong, stable, pragmatic, down-to-earth, reliable, dependable, hard-working, extracting, precise, methodical, conscientious, frugal, devoted, patriotic and trustworthy!"
    elif finalcount == 5:
        return "Your lucky number is " + str(finalcount) + " " + " and you are energetic, adventurous, daring and freedom-loving. They also tend to be versatile, flexible, adaptable, curious, social, sensual, quick-thinking, witty, courageous and worldly."
    elif finalcount == 6:
        return "Your lucky number is " + str(finalcount) + " " + " and you are responsible, loving, self-sacrificing, protective, sympathetic and compassionate. These loyal, maternal figures are domestic, fair and idealistic healers or teachers."
    elif finalcount == 7:
        return "Your lucky number is " + str(finalcount) + " " + ".7 isn't just a lucky number. It's also spiritual, intelligent, analytical, focused, introspective, studious, intuitive, knowledgeable, contemplative, serious, persevering, refined, gracious and displays much inner wisdom."
    elif finalcount == 8:
        return "Your lucky number is " + str(finalcount) + " " + " and you are authoritative, business-minded leaders. They value control and tend to be powerful, but are also balanced, materially detached, successful and realistic. They end up in management positions, are efficient, capable, street-smart and good judges of character."
    elif finalcount == 9:
        return "Your lucky number is " + str(finalcount) + " " + " and you are helpful, compassionate, aristocratic, sophisticated, charitable, generous, humanitarian, romantic, cooperative, creative, self-sufficient, proud and self-sacrificing."
    else:
        return "Your lucky number is " + str(finalcount)


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

    return getNumeroText(finalcount)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

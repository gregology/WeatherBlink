import urllib2, json, logging, re, os, time, datetime, thread
from math import exp
from pprint import pprint
from astral import *
import pytz

logger = logging.getLogger('WeatherBlink')
hdlr = logging.FileHandler('./fetch.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

logger.info('Start time')

# User variables
city = "zmw:00000.1.71063"
key = "236d258e67fc286e"
eastern = pytz.timezone('US/Eastern')
city_name = 'Ottawa'

logger.debug('city: ' + city)
logger.debug('key: ' + key)

def daytime():
    sunset = Astral()[city_name].sunset(datetime.datetime.now()).time()
    sunrise = Astral()[city_name].sunrise(datetime.datetime.now()).time()
    now = eastern.localize(datetime.datetime.now()).time()
    return sunrise < now < sunset


def fetch_weather():
    conditionsurl = ("http://api.wunderground.com/api/" + key + "/conditions/q/" + city + ".json")
    logger.debug('conditions url: ' + conditionsurl)

    alerturl = ("http://api.wunderground.com/api/" + key + "/alerts/q/" + city + ".json")
    logger.debug('alerts url: ' + alerturl)

    conditionsdata = json.load(urllib2.urlopen(conditionsurl))
    logger.debug('conditions loaded: ' + str(len(conditionsdata))) if len(conditionsdata) > 0 else logger.error('no conditions data loaded :(')
    logger.info('time of fetch: ' + conditionsdata[u'current_observation'][u'local_time_rfc822'])
    logger.info('current conditions: ' + conditionsdata[u'current_observation'][u'weather'])

    alertdata = json.load(urllib2.urlopen(alerturl))
    logger.debug('alerts loaded: ' + str(len(alertdata))) if len(alertdata) > 0 else logger.error('no alerts data loaded :(')
    logger.info('current alerts: ' + str(alertdata[u'alerts']))

    snowing = (True if re.search(r"\bsnow", conditionsdata[u'current_observation'][u'weather'], re.IGNORECASE) else False)
    raining = (True if re.search(r"\bdrizzle|\brain|\bshower", conditionsdata[u'current_observation'][u'weather'], re.IGNORECASE) else False)
    alerts  = (True if len(alertdata[u'alerts']) > 0 else False)
    cloudy  = (True if re.search(r"\bcloud", conditionsdata[u'current_observation'][u'weather'], re.IGNORECASE) or raining or snowing else False)

    global weather
    weather = {
        'time_string': conditionsdata[u'current_observation'][u'local_time_rfc822'],
        'timestamp':   conditionsdata[u'current_observation'][u'observation_epoch'],
        'conditions':  conditionsdata[u'current_observation'][u'weather'],
        'temp':        conditionsdata[u'current_observation'][u'temp_c'],
        'feelslike':   float(conditionsdata[u'current_observation'][u'feelslike_c']),
        'snowing':     snowing,
        'raining':     raining,
        'cloudy':      cloudy,
        'alerts':      alerts,
        'daytime':     daytime(),
    }

def ouput_weather():
    print "Current Weather"
    print "###############"
    print "Fetch time: " + weather['time_string']
    print "Conditions: " + weather['conditions']
    print "Temp: " + str(weather['temp']) + "C"
    print "Feels like: " + str(weather['feelslike']) + "C"
    print "Snowing: " + str(weather['snowing'])
    print "Raining: " + str(weather['raining'])
    print "Cloudy: " + str(weather['cloudy'])
    print "Day Time: " + str(weather['daytime'])
    print "Alerts: " + str(weather['alerts'])

# import ipdb; ipdb.set_trace()

fetch_weather()

ouput_weather()

with open('conditions.json', 'w') as outfile:
  json.dump(weather, outfile)

logger.info('End time\n\n\n')

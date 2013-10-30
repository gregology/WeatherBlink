import urllib2, json, logging, re, os, time, datetime, thread
from math import exp
from pprint import pprint

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

logger.debug('city: ' + city)
logger.debug('key: ' + key)

def fetch_weather():
    conditionsurl = ("http://api.wunderground.com/api/" + key + "/conditions/q/" + city + ".json")
    logger.debug('conditions url: ' + conditionsurl)
    
    alerturl = ("http://api.wunderground.com/api/" + key + "/alerts/q/" + city + ".json")
    logger.debug('alerts url: ' + alerturl)
    
    conditionsdata = json.load(urllib2.urlopen(conditionsurl))
    logger.debug('conditions loaded: ' + str(len(conditionsdata))) if len(conditionsdata) > 0 else logger.error('no conditions data loaded :(')
    logger.info('current conditions: ' + conditionsdata[u'current_observation'][u'weather'])
    
    alertdata = json.load(urllib2.urlopen(alerturl))
    logger.debug('alerts loaded: ' + str(len(alertdata))) if len(alertdata) > 0 else logger.error('no alerts data loaded :(')
    logger.info('current alerts: ' + str(alertdata[u'alerts']))
    
    snowing = (True if re.search(r"\bsnow", conditionsdata[u'current_observation'][u'weather'], re.IGNORECASE) else False)
    raining = (True if re.search(r"\bdrizzle|\brain|\bshower", conditionsdata[u'current_observation'][u'weather'], re.IGNORECASE) else False)
    alerts = (True if len(alertdata[u'alerts']) > 0 else False)

    global weather
    weather = {'conditions':conditionsdata[u'current_observation'][u'weather'], 'temp':conditionsdata[u'current_observation'][u'temp_c'], 'snowing':snowing, 'raining':raining, 'alerts':alerts}

def ouput_weather():
    print "Current Weather"
    print "###############"
    print "Conditions: " + weather['conditions']
    print "Temp: " + str(weather['temp']) + "C"
    print "Snowing: " + str(weather['snowing'])
    print "Raining: " + str(weather['raining'])
    print "Alerts: " + str(weather['alerts'])

fetch_weather()

ouput_weather()

with open('conditions.json', 'w') as outfile:
  json.dump(weather, outfile)

logger.info('End time\n\n\n')
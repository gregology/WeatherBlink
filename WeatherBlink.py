import urllib2, json, logging, re
from pprint import pprint

logger = logging.getLogger('WeatherBlink')
hdlr = logging.FileHandler('./wb.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

logger.info('Start time')

# User variables
city = "zmw:00000.1.71063"
key = "236d258e67fc286e"
cold = -5
warm = 10

logger.debug('city: ' + city)
logger.debug('key: ' + key)

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

snowing = (True if re.search(r"\bsnow", conditionsdata[u'current_observation'][u'weather']) else False)
raining = (True if re.search(r"\bdrizzle|\brain|\bshower", conditionsdata[u'current_observation'][u'weather']) else False)
alerts = (True if len(alertdata[u'alerts']) > 0 else False)

# Weather output
print "Current conditions: " + conditionsdata[u'current_observation'][u'weather']
print "Current temp: " + str(conditionsdata[u'current_observation'][u'temp_c']) + "C"
print "Number of alerts: " + str(len(alertdata[u'alerts']))
print "Snowing: " + str(snowing)
print "Raining: " + str(raining)
print "alerts: " + str(alerts)

logger.info('End time\n\n\n')
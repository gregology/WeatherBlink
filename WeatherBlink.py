import urllib2, json, logging, re, os, time, datetime, thread
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


def colour_limit(colour):
    return ( 0 if colour < 0 else ( 255 if colour > 255 else colour))


def temp_to_colour(temp):
    colourratio = (float(temp - cold) / float(warm - cold)) # returns ratio as float between cold and warm
    logger.debug('Using ' + str(colourratio) + ' as colour ratio')
    red = colour_limit(int(255 * (colourratio)*2))
    blue = colour_limit(int(255 * (0.7 - colourratio)*2))
    green = colour_limit(int((1-((4*colourratio**2)-4*colourratio+1))*255))
    logger.debug('red:' + str(red))
    logger.debug('green:' + str(green))
    logger.debug('blue:' + str(blue))
    return str(red) + "," + str(green) + "," + str(blue)


def blink(rgb):
    cmd = 'mkdir test' + rgb # ./blink1-tool --rgb ' + rgb + ' -ms 100 -t 0'
    logger.debug('Running ' + cmd)
    print 'blink: ' + rgb
    time.sleep(0.5)
#    os.system(cmd)


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


def blink_weather():
    while True:
      colour_temp = temp_to_colour(weather['temp'])
      if weather['alerts']:
        blink('255,0,0')
        blink('0,0,255')
      elif weather['snowing']:
        blink('255,255,255')
        blink(colour_temp)
      elif weather['raining']:
      	blink('0,0,255')
      	blink(colour_temp)
      else:
      	blink('0,0,0')
        blink(colour_temp)

def weather_updater():
    while True:
    	fetch_weather()
    	ouput_weather()
    	time.sleep(15)

fetch_weather()

ouput_weather()

try:
   thread.start_new_thread( weather_updater() )
   thread.start_new_thread( blink_weather() )
except:
   print "Error: unable to start thread"

while 1:
   pass


logger.info('End time\n\n\n')
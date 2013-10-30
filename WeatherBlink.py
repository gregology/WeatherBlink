import urllib2, json, logging, re, os, time, datetime, thread
from math import exp
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

#http://www.eldoradocountyweather.com/canada/climate2/Ottawa.html
avg_month_temp_ottawa = [-10.5, -8.6, -2.4, 6., 13.6, 18.4, 21., 19.7, 14.7, 8.2, 1.5, -6.6]
std_month_temp_ottawa = [2.9, 2.7, 2.5, 1.9, 1.8, 1.3,1.1,1.1,1.2,1.6,1.7,3.3]


logger.debug('city: ' + city)
logger.debug('key: ' + key)


def colour_limit(colour):
    return ( 0 if colour < 0 else ( 255 if colour > 255 else colour))


def temp_to_colour(temp):
    month = datetime.datetime.today().month
    #assume temperatures are normally distributed around the average that month.
    #given a temp, what is the CDF at that point, given the avg. temp and std. 
    monthly_avg = avg_month_temp_ottawa[month-1]
    monthly_std = std_month_temp_ottawa[month-1]
    colourratio = approx_standard_norm_cdf( (temp - monthly_avg)/monthly_std )
    logger.debug('Using ' + str(colourratio) + ' as colour ratio')
    red = colour_limit(int(255 * (colourratio)*2))
    blue = colour_limit(int(255 * (0.7 - colourratio)*2))
    green = colour_limit(int((1-((4*colourratio**2)-4*colourratio+1))*255))
    logger.debug('red:' + str(red))
    logger.debug('green:' + str(green))
    logger.debug('blue:' + str(blue))
    return str(red) + "," + str(green) + "," + str(blue)


def approx_standard_norm_cdf(x):
    if x >= 0:
      return 1 - 0.5*exp(-1.2*x**(1.3))
    else:
      return 0.5*exp(-1.2*(-x)**(1.3))


def blink(rgb, pause=0.5):
    cmd = './blink1-tool --rgb ' + rgb + ' -m 300'
    logger.debug('Running ' + cmd)
    print 'blink: ' + rgb
    os.system(cmd)
    time.sleep(pause)


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
        blink('255,0,0', pause=0.25)
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

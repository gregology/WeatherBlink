import urllib2, json, logging, re, os, time, datetime, thread
from math import exp
from pprint import pprint

logger = logging.getLogger('BlinkWeather')
hdlr = logging.FileHandler('./blink.log')
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


def blink(rgb, pause=0.5, fade=300):
    cmd = './../blink1/commandline/blink1-tool --rgb ' + rgb + ' -m ' + str(fade)
    logger.debug('Running ' + cmd)
    print 'blink: ' + rgb
    os.system(cmd)
    time.sleep(pause)


def fetch_weather():
    from pprint import pprint
    json_data=open('conditions.json')

    conditionsdata = json.load(json_data)
    json_data.close()

    global weather
    weather = {'fetch_time':conditionsdata[u'fetch_time'], 'conditions':conditionsdata[u'conditions'], 'temp':conditionsdata[u'temp'], 'snowing':conditionsdata[u'snowing'], 'raining':conditionsdata[u'raining'], 'alerts':conditionsdata[u'alerts']}


def ouput_weather():
    print "Current Weather"
    print "###############"
    print "Fetch time: " + weather['fetch_time']
    print "Conditions: " + weather['conditions']
    print "Temp: " + str(weather['temp']) + "C"
    print "Snowing: " + str(weather['snowing'])
    print "Raining: " + str(weather['raining'])
    print "Alerts: " + str(weather['alerts'])


def blink_weather():
    while True:
        fetch_weather()
        print weather
        for x in range(0, 60):
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


blink_weather()


logger.info('End time\n\n\n')

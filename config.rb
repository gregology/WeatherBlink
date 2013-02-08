#!/usr/bin/env ruby

# You can get a free wunder ground api key from http://www.wunderground.com/weather/api/
$wundergroundapikey = '1122334455667788'

# city code, it took me a while to find this for Ottawa, if you find a list please push it to this git repo :)
$citycode = 'zmw:00000.1.71063'

# What is cold? At what temp should the indicator turn blue
$cold = '-15'
$coldcolour = '0,0,255'

# Warm is inbetween hot and cold
$warmcolour = '255,165,0'

# What is hot? At what temp should the indicator turn red
$hot = '15'
$hotcolour = '255,0,0'

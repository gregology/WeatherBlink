#!/usr/bin/env ruby
require 'open-uri'
require 'rubygems'
require 'json'
require 'active_support/all'
require_relative 'config.rb'
include Comparable

def pull_conditions
  f = File.open('conditions.json', 'w')
  f.puts open('http://api.wunderground.com/api/'+$wundergroundapikey+'/conditions/q/'+$citycode+'.json') {|f| f.read }
  f.close
  system('chmod 777 conditions.json')
end

def pull_alerts
  f = File.open('alerts.json', 'w')
  f.puts open('http://api.wunderground.com/api/'+$wundergroundapikey+'/alerts/q/'+$citycode+'.json') {|f| f.read }
  f.close
  system('chmod 777 alerts.json')
end

def update_alerts
  file = File.open("alerts.json", "rb")
  alerts = file.read
  file.close
  parsed = JSON.parse(alerts)
  $alerts = parsed['alerts'][0]
end

def update_temp
  file = File.open("conditions.json", "rb")
  conditions = file.read
  file.close
  parsed = JSON.parse(conditions)
  $temp = parsed['current_observation']['temp_c']
end

def update_conditions
  file = File.open("conditions.json", "rb")
  conditions = file.read
  file.close
  parsed = JSON.parse(conditions)
  $conditions = parsed['current_observation']['weather']
end

def warm_ratio
  ($temp.to_f - $cold.to_f) / ($hot.to_f - $cold.to_f)
end

def blink_colour
  # A colour between blue and red though orange using warm_ratio
end

def is_snowing?
  return true if $conditions =~ /snow/i
end

def is_weather_alert?
  return true if !$alerts.nil?
end

def is_raining?
  return true if $conditions =~ /rain|drizzle|shower/i
end

# is_cold?, is_warm?, and is_hot? aren't really that useful, I might cut them away and make a colour method to create an accurate $colour
def is_cold?
  return true if $temp.to_f <= $cold.to_f
end

def is_warm?
  return true if $temp.to_f > $cold.to_f && $temp.to_f < $hot.to_f 
end

def is_hot?
  return true if $temp.to_f >= $hot.to_f
end

def blink(rgb)
  system('./blink1-tool --rgb ' + rgb.to_s + ' -ms 100 -t 0')
end

def display_conditions
  puts 'Conditions - ' + $conditions.to_s
  puts 'Temperature - ' + $temp.to_s
  puts 'WEATHER ALERT - ' + $alerts['description'].to_s if is_weather_alert?
end

def blink_warning
  blink('255,0,0')
  sleep(0.5)
  blink('0,0,255')
  sleep(0.5)
end

def blink_weather
  blink($colour)
  sleep(1.5)
  blink('255,255,255') if is_snowing?
  blink('0,255,255') if is_raining?
  sleep(0.5)
end

def pull_update
   while true
    pull_conditions
    pull_alerts
    update_temp
    update_conditions
    update_alerts
    puts 'Conditions and alerts updated!'
    sleep(10.minutes)
   end
end

def blinker
   while true
    display_conditions

    # this need to be rewritten to be pretty
    $colour = $coldcolour if is_cold?
    $colour = $warmcolour if is_warm?
    $colour = $hotcolour if is_hot?

    is_weather_alert? ? blink_warning : blink_weather
   end
end


t1=Thread.new{pull_update()}
t2=Thread.new{blinker()}
t1.join
t2.join


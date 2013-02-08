#!/usr/bin/env ruby
require 'open-uri'
require 'rubygems'
require 'json'
require_relative 'config.rb'
include Comparable

def pull_weather
  f = File.open('latest.json', 'w')
  f.puts open('http://api.wunderground.com/api/'+$wundergroundapikey+'/conditions/q/'+$citycode+'.json') {|f| f.read }
  f.close
  system('chmod 777 latest.json')
end

def update_temp
  file = File.open("latest.json", "rb")
  latest = file.read
  file.close
  parsed = JSON.parse(latest)
  $temp = parsed['current_observation']['temp_c']
end

def update_conditions
  file = File.open("latest.json", "rb")
  latest = file.read
  file.close
  parsed = JSON.parse(latest)
  $conditions = parsed['current_observation']['weather']
end

def warm_ratio
  ($temp.to_f - $cold.to_f) / ($hot.to_f - $cold.to_f)
end

def warm_colour
  # A colour between blue and red though orange using warm_ratio
end

def is_snowing?
  return true if $conditions =~ /snow|blizzard/i
end

def is_raining?
  return true if $conditions =~ /rain|drizzle|shower/i
end

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
  system('./blink1-tool --rgb ' + rgb.to_s)
end

pull_weather

  loop do
    update_temp
    update_conditions

    $colour = $coldcolour if is_cold?
    $colour = $warmcolour if is_warm?
    $colour = $hotcolour if is_hot?

    puts 'Conditions - ' + $conditions.to_s
    puts 'Temperature - ' + $temp.to_s

    blink($colour)
    sleep(1)
    blink('0,0,0') if is_snowing?
    sleep(0.5)

  end





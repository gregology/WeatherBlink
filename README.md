WeatherBlink
============

A Python weather indicator for Blink1 indtened to be run on a Raspberry Pi

![alt text](http://i.imgur.com/JaVcq7S.jpg "WeatherBlink blinking cold weather")

## Install instructions

### Install Raspbian

Download Raspbian [here](http://www.raspberrypi.org/downloads) and install on a 4Gb SD card as per the instuctions.

### Set static IP

Edit /etc/network/interfaces on the SD card. Something like this:

    # The loopback interface
    auto lo
    iface lo inet loopback
    auto eth0
    iface eth0 inet static
    # your static IP
    address 192.168.0.100
    # your gateway IP
    gateway 192.168.0.1
    netmask 255.255.255.0
    # your network address
    network 192.168.0.0
    broadcast 192.168.0.255

Boot up your Raspberry Pi with network and blink1 attached.

### Access Pi and setup system

From terminal ssh into your Pi (password will be "raspberry")

    $ ssh pi@192.168.0.100

Optionally run raspi-config to fill partitions, set timezones, change password etc.

    $ sudo raspi-config

Create code directory

    $ mkdir ~/code

### Build blink1 command-line tool from source

    $ sudo apt-get install libusb-1.0-0-dev
    $ cd ~/code
    $ git clone git://github.com/todbot/blink1.git
    $ cd blink1/commandline
    $ make
    $ sudo ./blink1-tool --on

[More instructions](https://github.com/todbot/blink1/wiki/Raspberry-Pi-and-blink(1))

### Install git

    $ cd ~/code
    $ git clone https://github.com/gregology/WeatherBlink.git

### Create init.d job

    $ sudo nano /etc/init.d/WeatherBlink

And add something like this

    #! /bin/sh
    # /etc/init.d/WeatherBlink

    # The following part always gets executed.
    echo "This part always gets executed"
    
    # The following part carries out specific functions depending on arguments.
    case "$1" in
      start)
        cd /home/pi/code/WeatherBlink/
        python BlinkWeather.py
        ;;
      stop)
        echo "Nothing really happens here"
        ;;
      *)
        echo "Usage: /etc/init.d/foobar {start|stop}"
        exit 1
        ;;
    esac
    
    exit 0

Then set permissions

    $ sudo chmod 755 /etc/init.d/WeatherBlink

### Create cron job

    $ crontab -e

Add this line

    */10 * * * * cd /home/pi/code/WeatherBlink; python FetchWeather.py

### Fetch weather and reboot pi

    $ cd ~/code/WeatherBlink; python FetchWeather.py
    $ sudo reboot

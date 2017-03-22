#!/usr/bin/python

# Main script for Adafruit Internet of Things Printer 2.  Monitors button
# for taps and holds, performs periodic actions (Twitter polling by default)
# and daily actions (Sudoku and weather by default).
# Written by Adafruit Industries.  MIT license.
#
# MUST BE RUN AS ROOT (due to GPIO access)
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, Image, socket
import datetime
from datetime import date
import filewalker
from Adafruit_Thermal import *
import os
from PIL import Image
import text2png_tester
from MessageClass import *
import random
import locale

print("Starting up....")
ledPin       = 18
buttonPin    = 23
holdTime     = 2     # Duration for button hold (shutdown)
tapTime      = 0.01  # Debounce time for button taps
nextInterval = 0.0   # Time of next recurring operation
dailyFlag    = False # Set after daily trigger occurs
lastId       = '1'   # State information passed to/from interval script
printer      = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

#get locale for date display
locale.setlocale(locale.LC_ALL, '')

# set item path
dir_path = os.path.dirname(os.path.realpath(__file__))
item_folder = dir_path + '/items'

# initialize item of the day
picked_item = ""

# Daytime to reset the printer to print the new message of the next day
hrs  = 4
mins = 0

# Called when button is briefly tapped.  Invokes time/temperature script.
def tap():
  print("Button press detected.")
  GPIO.output(ledPin, GPIO.HIGH)  # LED on while working
  #subprocess.call(["python", "collected_before.py"])
  #print today's message again
  if picked_item != "":
      printer.printImage(png_from_item(picked_item), True)
  GPIO.output(ledPin, GPIO.LOW)


# Called when button is held down.  Prints image, invokes shutdown process.
def hold():
  print("Button hold detected.")
  GPIO.output(ledPin, GPIO.HIGH)
  printer.printImage(Image.open('gfx/goodbye.png'), True)
  printer.feed(3)
  subprocess.call("sync")
  subprocess.call(["shutdown", "-h", "now"])
  GPIO.output(ledPin, GPIO.LOW)


# Called at periodic intervals (30 seconds by default).
# Invokes twitter script.
def interval():
  print("Twitter polled.")
  GPIO.output(ledPin, GPIO.HIGH)
  p = subprocess.Popen(["python", "twitter.py", str(lastId)],
    stdout=subprocess.PIPE)
  GPIO.output(ledPin, GPIO.LOW)
  return p.communicate()[0] # Script pipes back lastId, returned to main


# Called once per day (5:30am by default).
def daily():
  print("First button press of the day...")
  GPIO.output(ledPin, GPIO.HIGH)
  #subprocess.call(["python", "daily_message.py"])
#  output_image = Image.open(png_from_item(picked_item))
#  image_buffer = output_image.load()
  printer.printImage(png_from_item(picked_item), True)
  printer.feed(3)
  GPIO.output(ledPin, GPIO.LOW)

# takes a file path and return ready-to-print png image, converting text files by invoking MessageClass
def png_from_item(picked_item):
    if picked_item.rsplit(".",1)[1] == "png":
        print("Image printed...")
        print(picked_item)
        return Image.open(picked_item, True)
    elif picked_item.rsplit(".",1)[1] == "txt":
        textfile_handle = open(picked_item, "r")
        textfile_output = "".join(textfile_handle.readlines())
        random_font = ImageFont.truetype(random.choice(fonts), 14, encoding='unic')
        return Message(textfile_output,random.choice(Message_Style.values())).BuildMessage(random_font)

# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)

# Enable LED and button (w/pull-up on latter)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED on while working
GPIO.output(ledPin, GPIO.HIGH)

# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.

# Show IP address (if network is available)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	printer.print('My IP address is ' + s.getsockname()[0])
	printer.feed(3)
except:
	printer.boldOn()
	printer.println('Network is unreachable. Waiting 30 seconds...')
	printer.boldOff()
        time.sleep(30)
        try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 0))
		printer.print('My IP address is ' + s.getsockname()[0])
		printer.feed(3)
	except:
		printer.boldOn()
		printer.println('Network problems still occuring. Exiting...')
		printer.boldOff()
		printer.feed(3)
		exit(0)

# Print greeting image.
#printer.print('Started at ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
printer.printImage(Image.open('gfx/helloworld.png'), True)
printer.feed(3)
GPIO.output(ledPin, GPIO.LOW)
	
# Poll initial button state and time
prevButtonState = GPIO.input(buttonPin)
prevTime        = time.time()
tapEnable       = False
holdEnable      = False

print("Waiting for event....")

#initialize item to start with
# pick item of the day
picked_item = filewalker.pick_item(item_folder,date.today())

# Main loop
while(True):

  # Poll current button state and time
  buttonState = GPIO.input(buttonPin)
  t           = time.time()

  # Has button state changed?
  if buttonState != prevButtonState:
    prevButtonState = buttonState   # Yes, save new state/time
    prevTime        = t
  else:                             # Button state unchanged
    if (t - prevTime) >= holdTime:  # Button held more than 'holdTime'?
      # Yes it has.  Is the hold action as-yet untriggered?
      if holdEnable == True:        # Yep!
        hold()                      # Perform hold action (usu. shutdown)
        holdEnable = False          # 1 shot...don't repeat hold action
        tapEnable  = False          # Don't do tap action on release
    elif (t - prevTime) >= tapTime: # Not holdTime.  tapTime elapsed?
      # Yes.  Debounced press or release...
      if buttonState == True:       # Button released?
        if tapEnable == True:       # Ignore if prior hold()

          # Once per day (currently set for 6:30am local time, or when script
          # is first run, if after 5:30am), run forecast and sudoku scripts.
          if dailyFlag == False:
            daily()
            dailyFlag = True
          else:
            tap()                     # Tap triggered (button released)
          tapEnable  = False        # Disable tap and hold
          holdEnable = False
      else:                         # Button pressed
        tapEnable  = True           # Enable tap and hold actions
        holdEnable = True

  l = time.localtime()
  if (60 * l.tm_hour + l.tm_min) > (60 * hrs + mins) and (60 * l.tm_hour + l.tm_min) < (60 * hrs + mins + 2):
    dailyFlag = False
    #clear current item of the day by moving file to 'used' bin
  ###if picked_item != "":
  ###    move_to_bin(picked_item)    
    # pick item of the day
    picked_item = filewalker.pick_item(item_folder,date.today())
    print(picked_item)
    # print item of the day
    printer.printImage(png_from_item(picked_item), True)
    printer.feed(3)
    

  # LED blinks while idle, for a brief interval every 2 seconds.
  # Pin 18 is PWM-capable and a "sleep throb" would be nice, but
  # the PWM-related library is a hassle for average users to install
  # right now.  Might return to this later when it's more accessible.
  if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15) and dailyFlag == False:
    GPIO.output(ledPin, GPIO.HIGH)
  else:
    GPIO.output(ledPin, GPIO.LOW)

  # Every 30 seconds, run Twitter scripts.  'lastId' is passed around
  # to preserve state between invocations.  Probably simpler to do an
  # import thing.
  if t > nextInterval:
    nextInterval = t + 30.0
    result = interval()
    if result is not None:
      lastId = result.rstrip('\r\n')


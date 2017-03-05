#!/usr/bin/python

from Adafruit_Thermal import *
import os 
import Image
import filewalker

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

dir_path = os.path.dirname(os.path.realpath(__file__))
picture_folder = dir_path + '/pics'

#printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
#printer.println(filewalker.pick_random_pic(picture_folder))
printer.printImage(Image.open(filewalker.pick_random_pic(picture_folder)), True)
printer.feed(3)



printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults

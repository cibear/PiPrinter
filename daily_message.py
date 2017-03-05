#!/usr/bin/python

from Adafruit_Thermal import *
import os 
import Image
import filewalker
from datetime import date

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

dir_path = os.path.dirname(os.path.realpath(__file__))
item_folder = dir_path + '/items'

#printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
#printer.println(filewalker.pick_random_pic(item_folder))
picked_item = filewalker.pick_item(item_folder,date.today())

#process according to file type
if picked_item.rsplit(".",1)[0] == "png":
    printer.printImage(Image.open(filewalker.pick_item(item_folder)), True)
elif picked_item.rsplit(".",1)[0] == "txt":
    textfile_handle = open("testfile.text", "r") 
    #print textfile_handle.read()
    printer.print(textfile_handle.read()) 
printer.feed(3)
#clean up by moving picked item to bin folder
#filewalker.move_to_bin(picked_item)


printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults

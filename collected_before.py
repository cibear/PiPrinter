#!/usr/bin/python

from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
printer.println("Collected before!")

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults

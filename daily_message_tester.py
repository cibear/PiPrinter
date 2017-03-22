#!/usr/bin/python

###from Adafruit_Thermal import *
import os 
from PIL import Image
import filewalker
from datetime import date
import text2png_tester
from MessageClass import *
import random

###printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

dir_path = os.path.dirname(os.path.realpath(__file__))
item_folder = dir_path + '/items'
#item_folder = "C:/Users/Christian/Documents/GitHub/PiPrinter/items"

print "Script started..."

###printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
#printer.println(filewalker.pick_random_pic(item_folder))


# takes a file path and return ready-to-print png image, converting text files by invoking MessageClass
def png_from_item(picked_item):
    if picked_item.rsplit(".",1)[1] == "png":
        print "Image printed..."
        return Image.open(picked_item)
    elif picked_item.rsplit(".",1)[1] == "txt":
        textfile_handle = open(picked_item, "r")
        textfile_output = "".join(textfile_handle.readlines())
        random_font = ImageFont.truetype(random.choice(fonts), 14, encoding='unic')
        return Message(textfile_output,random.choice(Message_Style.values())).BuildMessage(random_font)


# choose a file
picked_item = filewalker.pick_item(item_folder,date.today())

#convert to png
png_from_item(picked_item).show()


#process according to file type
# print "picked item: " + picked_item
# print picked_item.rsplit(".",1)[1]
# print "png?" + str(picked_item.rsplit(".",1)[1] == "png")
# print "txt?" + str(picked_item.rsplit(".",1)[1] == "txt")

# if picked_item.rsplit(".",1)[1] == "png":
#     ###printer.printImage(Image.open(filewalker.pick_item(item_folder)), True)
#     print "Image printed..."
# elif picked_item.rsplit(".",1)[1] == "txt":
#     textfile_handle = open(picked_item, "r")
#     textfile_output = "".join(textfile_handle.readlines())
#     #print textfile_output
#     print textfile_output
#     XX = Message(textfile_output,random.choice(Message_Style.values()))
#     XX.print_me()
#     #XY = Message("This is the text! I see what you did there...",Message_Style["Schweinchen"])
#     random_font = ImageFont.truetype(random.choice(fonts), 14, encoding='unic')
#     #XX.BuildMessage(random_font).show()
#     Message(textfile_output,random.choice(Message_Style.values())).BuildMessage(random_font).show()
#     #returned_image = msg_block2png(Message, font, wrap_limit, offset_x, offset_y)
    
    ###printer.println('Now printing text file:')
    ###printer.println(textfile_output)
###printer.feed(3)
#clean up by moving picked item to bin folder
#filewalker.move_to_bin(picked_item)


###printer.sleep()      # Tell printer to sleep
###printer.wake()       # Call wake() before printing again, even if reset
###printer.setDefault() # Restore printer to defaults

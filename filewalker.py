import os
import sys
import copy
import random
from datetime import date

#error class that handles exceptions in pick_item routine
class ItemPickException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

       
#picks an item (text, png...) from item_folder by date ("YYYY-MM-DD.*", or if none given, randomly, and returns full file path
def pick_item(item_folder, chosen_date = 0):
    #print "Hello World!"

    file_list = []
    
    for dirname, dirnames, filenames in os.walk(item_folder):
        #print 'Active folder:'+dirname
        # print all filenames.
        f=1
        for filename in filenames:
            #print '['+`f`+'] ' + filename
            f=f+1
            file_list.append(filename)
            #is the file name the same as the given date? then return date-specific item
            if filename.split(".")[0] == str(chosen_date):
                return item_folder+"/"+filename
        #once top level folder is run through, choose:
        if len(file_list) < 1:
            raise ItemPickException("No items left in folder!")
        else:
            i = random.choice(file_list)
            #return chosen file
            return item_folder+"/"+i
        break   #break after top level folder, don't recurse into subfolders
 
#moves a specific file to a new subfolder bin_folder (standard: "used")
def move_to_bin(filetomove,bin_folder = "used"):
    print filetomove.rsplit('/', 1)[0] + "/"+bin_folder + "/"+filetomove.rsplit('/', 1)[1]
    os.rename(filetomove, filetomove.rsplit('/', 1)[0] + "/"+bin_folder + "/"+filetomove.rsplit('/', 1)[1])
    

import os
import sys
import copy
import random

standard_folder = "C:/Users/Christian/Documents/GitHub/PiPrinter/pics"

def pick_random_pic(picture_folder):
    #print "Hello World!"
    

    file_list = []
    
    for dirname, dirnames, filenames in os.walk(standard_folder):
        #print 'Active folder:'+dirname
        # print all filenames.
        f=1
        for filename in filenames:
            #print '['+`f`+'] ' + filename
            f=f+1
            file_list.append(filename)
              
        #once top level folder is run through, choose:
        if len(file_list) < 1:
            print "no files in folder"
        else:
            i = random.choice(file_list)
            #process chosen file
            #print i
            os.rename(standard_folder+"/"+i, standard_folder+"/used_pics/"+i)
            return standard_folder+"/used_pics/"+i
        break   #break after top level folder, don't recurse into subfolders
 


#pick_random_pic(standard_folder)


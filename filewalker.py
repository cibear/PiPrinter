import os
import sys
import copy
import random

def pick_random_pic(picture_folder):
    #print "Hello World!"

    file_list = []
    
    for dirname, dirnames, filenames in os.walk(picture_folder):
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
            print(picture_folder+"/"+i)
            print(picture_folder+"/used_pics/"+i)
            os.rename(picture_folder+"/"+i, picture_folder+"/used_pics/"+i)
            return picture_folder+"/used_pics/"+i
        break   #break after top level folder, don't recurse into subfolders
 


#pick_random_pic(standard_folder)


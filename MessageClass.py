
from PIL import Image, ImageFont, ImageDraw
import textwrap
from datetime import date
import locale
from PIL._imaging import font
from MessageClass import *
import random
import os

### error handling
#error class that handles exceptions in pick_item routine
class GeneralException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg
#########################

fonts = ["ArialBd.ttf","Verdana.ttf","ELEPHNT.TTF"]

# define usable fonts
font = ImageFont.truetype('ArialBd.ttf', 14, encoding='unic')
header_font = ImageFont.truetype('Verdana.ttf', 14, encoding='unic')
font2 = ImageFont.truetype('ELEPHNT.ttf', 14, encoding='unic')

# stores pictures usable for messages
symbol_folder = os.path.dirname(os.path.realpath(__file__)) + "/symbols"
Pics = []

#populate Pics list with symbols
for dirname, dirnames, filenames in os.walk(symbol_folder):
    for filename in filenames:
        if filename.split(".")[1] == "png":
            Pics.append(os.path.join(dirname,filename))

#Pics["Rose"]="gfx/rose2.png"
#Pics["Schweinchen"]="gfx/Schweinchen.png"
#Pics["Kalender"]="gfx/calendar.png"



LEFT = 1
CENTER = 2
RIGHT = 3


msg_spacer = 10         # optional feed spacer between text elements
msg_header = "~~~~~~~~~ {:%d. %B %Y} ~~~~~~~~~".format(date.today())
msg_bottom = "~~~~~~~~~~~~~~~~~~~~~~~~~~~"

# Message Styles
Message_Style = {
#    "Rose":[[msg_header,header_font], msg_spacer, ["png",Pics['Rose']], 30, "text", msg_spacer, [msg_bottom,header_font]],
#    "Schweinchen":[[msg_header,header_font], msg_spacer, ["png",Pics['Schweinchen']], 30, "text", msg_spacer, [msg_bottom,header_font]],
    "Random":[[msg_header,header_font], msg_spacer, ["png",random.choice(Pics)], 30, "text", msg_spacer, [msg_bottom,header_font]]
}


def align_x_left(line_x,canvas_x=1000):
    return 0

def align_x_center(line_x,canvas_x=1000):
    return (canvas_x/2) - (line_x / 2)

def align_x_right(line_x,canvas_x=1000):
    return canvas_x - line_x

class Message:
    def __init__(self,text,message_structure):
        self.text = text
        self.message_structure = message_structure
        for index, element in enumerate(self.message_structure):
            if element == "text":
                self.message_structure[index] = self.text
   
    def print_me(self):
        print self.message_structure

    # print text for real
    def BuildMessage(self,font,wrap_limit=-1,offset_x=0,offset_y=0,file_handle='stdout.png',align=CENTER):
        # turns a series of strings, feeders or picutres to a finished message block in png format
    
        # initialize image
        canvas_x = canvas_y = 1000
        image = Image.new("1", [canvas_x,canvas_y], "white") # Working 'background' image
        draw = ImageDraw.Draw(image)
        
        #assign alignment calculation
        if align == LEFT:
            align_type = align_x_left
        elif align == CENTER:
            align_type = align_x_center
        elif align == RIGHT:
            align_type = align_x_right
            offset_x = -offset_x
        
        x_text = offset_x   # initialize tracker for offset + textblock height
        y_text = offset_y   
        # parse message components and collate
        for element in self.message_structure:
            print str(element) + "     " + str(x_text) + " " + str(y_text)
            active_font = font  # sets or resets font (font can change if passed along with string as tuple)
            if isinstance(element,list):           # element contains complex info, e.g. a graph with element = (filetype, path), or a specially formatted string as element = (string, font)
                if element[0] == "png":              # consider png file with path in element[1]
                    try:
                        img     = Image.open(element[1])
                        image.paste(img, (align_type(img.size[0],canvas_x)+offset_x,y_text))
                        y_text += img.size[1]           # read image y size and add to counter
                    except GeneralException:
                        print "Could not open file '%x'passed as message component",element[1]
                        raise
                elif isinstance(element[0], basestring):  # consider all other strings in element[0] as text/font tuples
                    try:
                        active_font = element[1]    # set passed font as active font
                    except GeneralException:
                        active_font = font
                        print "Could not process font."
                        raise
                    element = element[0]  # dissolve tuple by assigning string (for further processing below

            if isinstance(element, basestring):  # is string?
                # deconstruct string: 1) line break 2) word wrap
                text_lines = element.splitlines()
                output_lines = []
                if len(text_lines)>1:
                    for line in text_lines:
                        if wrap_limit > 0:
                            output_lines.append(textwrap.wrap(line, width=wrap_limit))
                        else:
                            output_lines.append(line)
                else:
                    if wrap_limit > 0:
                        output_lines.append(textwrap.wrap(text_lines[0], width=wrap_limit))
                    else:
                        output_lines = text_lines    
            
                for line in output_lines:
                    width, height = active_font.getsize(line)
                    draw.text((align_type(width,canvas_x)+offset_x, y_text), line, font=active_font)
                    y_text += height
                    x_text = max(x_text,width)  # if line is longer than those before, this is the new max.
                 

            elif isinstance(element, (int,long)): # is feeder?
                y_text += element
    
        # crop
        if align == LEFT:
            crop_image = image.crop((0,0,x_text+offset_x, y_text+offset_y))
        elif align == CENTER:
            crop_image = image.crop((canvas_x/2 - (x_text/2),0,canvas_x/2 + (x_text/2) +offset_x, y_text+offset_y))
        elif align == RIGHT:
            crop_image = image.crop((canvas_x - (x_text), 0, canvas_x, y_text+offset_y))
    
        # save output file
        crop_image.save(file_handle)
        return crop_image
    
    
# class Rose_Message("Hallo\n This is it!",[[msg_header,header_font], msg_spacer, ["png",Pics['Rose']], 30, "text", msg_spacer, [msg_bottom,header_font]]):
#         def print_me(self):
#             print


#X = Message("This is the text!",Message_Style["Rose"])

#X.print_me()

    
    
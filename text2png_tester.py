#coding=utf-8

from PIL import Image, ImageFont, ImageDraw
import textwrap
from datetime import date
import locale
from PIL._imaging import font
from MessageClass import *

### error handling
#error class that handles exceptions in pick_item routine
class GeneralException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg
#########################

LEFT = 1
CENTER = 2
RIGHT = 3

#locale.setlocale(locale.LC_ALL, 'deu_deu')  ## may need fixing/porting under Raspian/Linux (de_DE?)

# # define usable fonts
# font_folder = "library/fonts/"
# 
# font = ImageFont.truetype(font_folder+'ArialBd.ttf', 14, encoding='unic')
# header_font = ImageFont.truetype(font_folder+'Verdana.ttf', 14, encoding='unic')
# 
# # stores pictures usable for messages
# Pics = {}
# Pics["Rose"]="gfx/rose2.png"
# Pics["Schweinchen"]="gfx/Schweinchen.png"


output_string = "Hallo Welt! Dies ist meine offizielle Nachricht für den Printer. Ich hoffe sie wird auch gedruckt"
text = output_string.decode('utf-8')
wrap_limit = 40 #character limit per line
offset_x = 10
offset_y = 10
msg_spacer = 10         # optional feed spacer between text elements
msg_header = "~~~~~~~~~ {:%d. %B %Y} ~~~~~~~~~".format(date.today())
msg_bottom = "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
#Rose_Message = ((msg_header,header_font), msg_spacer, ("png",Pics['Rose']), 30, text, msg_spacer, (msg_bottom,header_font))
#Schweinchen_Message = ((msg_header,header_font), msg_spacer, ("png",Pics['Schweinchen']), 30, text, msg_spacer, (msg_bottom,header_font))

#Message = Rose_Message


#font_path = '/library/fonts/ARIAL.TTF'
#font = ImageFont.truetype(font_path, 14, encoding='unic')



# Calculate text_block dimensions
def get_textblock_size(text, font, wrap_limit=-1):
    if wrap_limit >0:
        lines = textwrap.wrap(text, width=wrap_limit)
    else:
        lines = text   
    y_text = 0     # keeps track of total height of finished textblock
    x_text = 0     # keeps track of max. width of finished textblock
    for line in lines:
        y_text += font.getsize(line)[1]               #adds to the y size
        x_text = max(x_text,font.getsize(line)[0])   #is this the biggest line?
    #print "x: "+str(x_text)+ " y: "+ str(y_text)
    return x_text, y_text


def align_x_left(line_x,canvas_x=1000):
    return 0

def align_x_center(line_x,canvas_x=1000):
    return (canvas_x/2) - (line_x / 2)

def align_x_right(line_x,canvas_x=1000):
    return canvas_x - line_x


    


# print text for real
def msg_block2png(Message_components,font,wrap_limit=-1,offset_x=0,offset_y=0,file_handle='stdout.png',align=CENTER):
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
    for element in Message_components:
        active_font = font  # sets or resets font (font can change if passed along with string as tuple)
        if isinstance(element,tuple):           # element contains complex info, e.g. a graph with element = (filetype, path), or a specially formatted string as element = (string, font)
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
            lines = textwrap.wrap(element, width=wrap_limit) 
            for line in lines:
                print line, y_text
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


#XX = Message("This is the text!",Message_Style["Rose"])

#XX.print_me()

#returned_image = msg_block2png(Message, font, wrap_limit, offset_x, offset_y)
#returned_image.show("Returned Image")

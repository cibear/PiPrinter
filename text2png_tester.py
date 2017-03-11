#coding=utf-8

from PIL import Image, ImageFont, ImageDraw
import textwrap
from datetime import date
import locale
from PIL._imaging import font

### error handling
#error class that handles exceptions in pick_item routine
class GeneralException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg
#########################



locale.setlocale(locale.LC_ALL, 'deu_deu')  ## may need fixing/porting under Raspian/Linux (de_DE?)

font = ImageFont.truetype('ArialBd.ttf', 14, encoding='unic')
header_font = ImageFont.truetype('Verdana.ttf', 20, encoding='unic')

output_string = "Hallo Welt! Dies ist meine offizielle Nachricht für den Printer. Ich hoffe sie wird auch gedruckt"
text = output_string.decode('utf-8')
wrap_limit = 40 #character limit per line
offset_x = 10
offset_y = 10
msg_spacer = 10         # optional feed spacer between text elements
msg_header = "~~~~~~~~~~ {:%d. %B %Y} ~~~~~~~~~~".format(date.today())
msg_bottom = "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
Message_components = ((msg_header,header_font), msg_spacer, text, msg_spacer, msg_bottom)

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




    


# print text for real
def msg_block2png(Message_components,font,wrap_limit=-1,offset_x=0,offset_y=0,file_handle='stdout.png'):
    # turns a series of strings, feeders or picutres to a finished message block in png format
    active_font = font  # sets font (font can change if passed along with string as tuple)
    # calculate final output dimensions
    x_text = y_text = 0
    for element in Message_components:
        if isinstance(element,tuple):           # element contains complex info, e.g. a graph with element = (filetype, path), or a specially formatted string as element = (string, font)
            if element[0] == "png":              # consider png file with path in element[1]
                try:
                    img     = Image.open(element[1])
                    y_text += img.size[1]           # read image y size and add to counter
                except GeneralException:
                    print "Could not open file '%x'passed as message component",element[1]
                    raise
            elif isinstance(element, basestring):  # consider all other strings in element[0] as text/font tuples
                try:
                    active_font = element[1]    # set passed font as active font
                except GeneralException:
                    active_font = font
                    print "Could not process font."
                    raise
                element = element[0]  # dissolve tuple by assigning string (for further processing below
        if isinstance(element, basestring):  # is string?
            delta_x, delta_y = get_textblock_size(element, active_font, wrap_limit)
            x_text = max(x_text,delta_x)      #biggest x defines textblock width
            y_text += delta_y
        elif isinstance(element, (int,long)): # is feeder?
            y_text += element
    # initialize image
    image = Image.new("1", [x_text+offset_x, y_text+offset_y], "white") # Working 'background' image
    draw = ImageDraw.Draw(image)
    # start the output
    y_text = offset_y   # reeinitialize tracker for offset + textblock height
    # iterate through message elements
    for element in Message_components:
        if isinstance(element, basestring):   # add message component
            lines = textwrap.wrap(element, width=wrap_limit) 
            for line in lines:
                print line, y_text
                width, height = font.getsize(line)
                draw.text((offset_x, y_text), line, font=font)
                y_text += height
        if isinstance(element, (int,long)):   # add spacer
            y_text += element    
    # save output file
    image.save(file_handle)

print "What?: "+str(get_textblock_size("Hello my name is Dr. Greenthumb", font))
msg_block2png(Message_components, font, wrap_limit, offset_x, offset_y)

#draw.text((10, 25), text, font=font)
#image.show()

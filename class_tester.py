from MessageClass import *


from PIL import Image, ImageFont, ImageDraw
import textwrap
from datetime import date
import locale
from PIL._imaging import font



# define usable fonts
font = ImageFont.truetype('ArialBd.ttf', 14, encoding='unic')

XX = Message("This is the text!",Message_Style["Rose"])
XY = Message("This is the text! I see what you did there...",Message_Style["Schweinchen"])
XX.print_me()

XX.BuildMessage(font)
XY.BuildMessage(font).show()
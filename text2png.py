from PIL import Image,ImageDraw  
import os,math

##############################
# process: get the string, parse into characters, pull individual characters together and output png
##############################

def text2png(fontpath,out,padding=1):
    imgs=[]
    min_width,max_width,min_height,max_height=-1,-1,-1,-1
    for infile in os.listdir(path):
        f,ext=os.path.splitext(infile)
        if ext== ".png":
            im=Image.open(os.path.join(path,infile))
            imgs.append(im)
            min_width = im.size[0] if min_width<0 else  min(min_width,im.size[0])
            max_width = im.size[0] if max_width<0 else  max(max_width,im.size[0])
            min_height = im.size[1] if min_height<0 else  min(min_height,im.size[0])
            max_height = im.size[1] if max_height<0 else  max(max_height,im.size[0])
    #calculate the column and rows
    num = len(imgs)
    column_f = math.ceil(math.sqrt(num))
    row_f = math.ceil(num / column_f)

    column = int(column_f)
    row = int(row_f)

    #out image
    box=(max_width + padding*2,max_height + padding*2)
    out_width = row * box[0]
    out_height = column * box[1]

    //out_image=Image.new('L', (out_width,out_height), color=transparent)
    out_image=Image.new("RGB", (out_width, out_height))
    for y in range(row):
        for x in range(column):
            index = (y * column) + x
            if index < num:
                out_image.paste(imgs[index],(x * box[0],y * box[1]))
    out_image.save(out)

combine_images('icon','t.png')
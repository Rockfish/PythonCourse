import math
import datetime

# Requires the Python Image Library from http://www.pythonware.com/products/pil/
# For documentation see http://effbot.org/imagingbook/
from PIL import Image, ImageDraw

def plot_year( ):
    width = 2
    height = 30

    im = Image.new("RGB", (365 * width + 3, height + 10), '#ffffff')
    draw = ImageDraw.Draw(im)
    
    caldata = [(1, 32, '#ffffa0'), 
               (33, 61, '#a0ebff'), 
               (62, 92, '#ebe0ff'),
               (93, 122, '#ffffa0'), 
               (123, 153, '#a0ebff'), 
               (154, 183, '#ebe0ff'),
               (184, 214, '#ffffa0'), 
               (215, 245, '#a0ebff'), 
               (246, 275, '#ebe0ff'),
               (276, 306, '#ffffa0'), 
               (307, 336, '#a0ebff'), 
               (337, 365, '#ebe0ff')]
    
    for (x1, x2, c) in caldata:
        q1 = (x1 * width)
        q2 = (x2 * width) + width
        draw.rectangle((q1, 0, q2, height + 9), fill=c)
    
    data = [10 for y in range(0,365)]

    for y in range(0, 364, 7):
        data[y + 1] = 5
        
    for (y, x) in zip(data, range(0, len(data)*width, width)):
        x = x + 2
        if y == 5:
            draw.line((x, height + 5, x, y), fill='red')
        else:
            draw.line((x, height, x, y), fill='#333333')

    data = [((13 * 7 * width) + width - 2) * q for q in range(0, 4)]
    
    for q in data:
        draw.rectangle((q, 0, q + (13 * 7 * width) + width - 2, height - 10), outline='black')

    for x in [93, 184, 276, 366]:
        draw.rectangle((0, 0, x * width, height + 9), outline='blue')
    
    (y, w, d) = datetime.date.isocalendar(datetime.datetime.now())
    
    x = ((w - 1) * 7 + d) * width + width
    
    draw.polygon((x-4, 0, x, 10, x+4, 0), fill='red')
    
    draw.polygon((x-4, height+10, x, height+1, x+4, height+10), fill='red')
    
    # clean up drawing surface
    del draw
    
    # Save image to a file                            
    im.save("Test.png", "PNG")
    
    # Saving to a buffer. Can be use to send pics to http clients.
    # f = StringIO.StringIO()
    # im.save(f, "PNG")
    # return f.getvalue()



if __name__ == "__main__":
    plot_year()



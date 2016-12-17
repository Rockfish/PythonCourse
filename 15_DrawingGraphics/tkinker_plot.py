
import math
from Tkinter import *
import time
import datetime


def point(tick, range, radius):
    angle = tick * (360.0 / range)
    radiansPerDegree = math.pi / 180
    pointX = int( round( radius * math.sin(angle * radiansPerDegree) ))
    pointY = int( round( radius * math.cos(angle * radiansPerDegree) ))
    return (pointX, pointY)


def circle(points, radius, centerX, centerY, slow=0):

    canvas.delete('lines')
    canvas.delete('points')

    for i in range(points):
        x, y = point(i+1, points, radius-4)
        scaledX, scaledY = (x + centerX), (centerY - y)
        canvas.create_line(centerX, centerY, scaledX, scaledY, tag='lines')
        canvas.create_rectangle(scaledX-2, scaledY-2,
                                scaledX+2, scaledY+2,
                                fill='red', tag='points')
        if slow: 
            canvas.update( )


def plotter( ):
    canvas.delete('lines')
    canvas.delete('points')
    circle(scaleVar.get(), (Width / 2), originX, originY, checkVar.get( ))

def lineplot( ):
    canvas.delete('lines')
    canvas.delete('points')
    canvas.create_rectangle(10, 10, Width-10, 30, fill='red', tag='points')

def plot_year( ):
    canvas.delete('lines')
    canvas.delete('points')

    width = 2
    height = 30
   
    caldata = [(1, 32, '#ffffa0'), (33, 61, '#a0ebff'), (62, 92, '#ebe0ff'),
               (93, 122, '#ffffa0'), (123, 153, '#a0ebff'), (154, 183, '#ebe0ff'),
               (184, 214, '#ffffa0'), (215, 245, '#a0ebff'), (246, 275, '#ebe0ff'),
               (276, 306, '#ffffa0'), (307, 336, '#a0ebff'), (337, 365, '#ebe0ff')]
    
    for (x1, x2, c) in caldata:
        q1 = (x1 * width)
        q2 = (x2 * width) + width
        canvas.create_rectangle(q1, 10, q2, height + 9, fill=c, tag='points')
    
    data = [10 for y in range(0,365)]

    for y in range(0, 364, 7):
        data[y + 1] = 5
        
    for (y, x) in zip(data, range(0, len(data)*width, width)):
        x = x + 2
        if y == 5:
            canvas.create_line(x, height+5, x, y + 10, fill='red')
        else:
            canvas.create_line(x, height, x, y + 10, fill='#333333', tag='points')

    for x in [93, 184, 276, 366]:
        canvas.create_rectangle(2, 10, x * width, height + 9, outline='blue', tag='points')
    
    # Add date arrow
    (y, w, d) = datetime.date.isocalendar(datetime.datetime.now())

    x = ((w-1) * 7 + d) * width + width

    canvas.create_polygon(x-4, 10, x, 20, x+4, 10, fill='red')
    canvas.create_polygon(x-4, height+9, x, height+1, x+4, height+9, fill='red')
    

def makewidgets( ):
    global canvas, scaleVar, checkVar

    canvas = Canvas(width=800, height=200)
    canvas.pack(side=TOP)
    
    scaleVar = IntVar( )
    checkVar = IntVar( )

    scale = Scale(label='Points on circle', variable=scaleVar, from_=1, to=360)
    scale.pack(side=LEFT)

    Checkbutton(text='Slow mode', variable=checkVar).pack(side=LEFT)

    Button(text='Plot', command=plotter).pack(side=LEFT, padx=20)

    Button(text='Line', command=lineplot).pack(side=LEFT, padx=20)

    Button(text='Year', command=plot_year).pack(side=LEFT, padx=20)

    # plot_year()

if __name__ == '__main__':
    Width = 800                        # default width, height
    if len(sys.argv) == 2: 
        Width = int(sys.argv[1])       # width cmdline arg
    
    originX = originY = Width / 2      # same as circle radius
    makewidgets( )                     # on default Tk root
    mainloop( )


import random
import math

def squares(vsk, x, y, size, count):
    # vsk.rectMode("center")
    vsk.rectMode("corner")
    vsk.pushMatrix()
    vsk.translate(x,y)
    for k in range(count):
        w = vsk.random(1,size)
        h = vsk.random(1,size)
        # print(x,y, w, h)
        vsk.rect(x, y, w, h)
    vsk.popMatrix()


def filledSquares(vsk, x, y, size, count):        
    vsk.pushMatrix()
    vsk.rectMode("corner")
    for sq in range(count):
        w = vsk.random(1,size)
        h = vsk.random(1,size)
        x = vsk.random(1,x)
        y = vsk.random(1,y)
        # vsk.penWidth("1mm", 2)  #
        # vsk.fill(1)
        vsk.translate(x,y)
        vsk.rect(x, y, w, h)
    vsk.popMatrix()


def stackSquares(vsk, x, y, size, count):        
    vsk.pushMatrix()
    vsk.rectMode("corner")
    for sq in range(count):
        w = sq*size*0.3
        h = sq*size*0.3
        xx = sq*x*0.9
        yy = vsk.random(-size,size)

        # vsk.penWidth("1mm", 2)  #
        # vsk.fill(1)
        # vsk.translate(x,y)

        vsk.rect(xx+x, yy+y, w, h)
    vsk.popMatrix()

    # for _ in range(5):        
    #     vsk.pushMatrix()            
    #     vsk.rotate(_*5, degrees=True)
    #     vsk.rect(-2, -2, 2, 2)
    #     vsk.popMatrix()
    #     vsk.translate(5, 0)


def fillsquare(vsk, xoffset,yoffset,width,height,angle,interval,outline):
    if (outline == 1):
        vsk.rect(xoffset,yoffset,width,height)
    for x in range(int(width/interval)):
        vsk.line(xoffset+x*interval,yoffset+0,xoffset+x*interval,yoffset+height )



def subdivpattern(vsk,xoffset,yoffset,width,height,generations,numtypes):
    # types = [0.60, 0.65, 0.75, 0.64, 0.80]
    types = [1.60, 2.65, 0.75, 3.64, 0.80]
    # zones = [[[0,0,width,height], [100,100,130,130]]]
    zones = [ [[0,0,width,height]] ]
    # zones = [ [[0, 0, 10000, 10000]], [[[0, 0, 8692, 6689], [0, 6689, 8692, 10000], [8692, 6689, 10000, 10000], [8692, 0, 10000, 6689]]]]

    for gen in range(generations):
        zones.append([])
        for sq in zones[gen]:
            #print(zones[gen])
            #print(sq[0], sq[1])
            # x = random.randint((sq[2]-sq[0])/2-width/10,(sq[2]-sq[0])/2+width/10)
            # y = random.randint((sq[3]-sq[1])/2-height/10 ,(sq[3]-sq[1])/2+height/10)
            print(sq[0],sq[2]-sq[0])
            print(sq[1],sq[3]-sq[1])
            # x = (sq[2]-sq[0])/2 + random.randrange(-500,500)
            # y = (sq[3]-sq[1])/2 + random.randrange(-500,500)
            x = vsk.random(int(sq[0]),int(sq[0]+(sq[2]-sq[0])/2))
            y = vsk.random(int(sq[1]),int(sq[1]+(sq[3]-sq[1])/2))
            zones[gen+1].append([sq[0],sq[1],x,y])
            zones[gen+1].append([sq[0],y,x,sq[3]])
            zones[gen+1].append([x,y,sq[2],sq[3]])
            zones[gen+1].append([x,sq[1],sq[2],y])
            # print("printing Zones")
            # print(zones)
    # for idx,z in enumerate(zones):
    for idx,s in enumerate(zones[generations]):
        if idx < 2:
            filltype = types[1]
        else:
            filltype = types[int(vsk.random(0,4))]
        fillsquare(vsk,xoffset+s[0],yoffset+s[1],s[2]-s[0],s[3]-s[1],90,filltype,0)
        # transforms.offset(r, (s[0],s[1]))
        # p.append(r)
        # plotter.select_pen(idx+1)

    # return p


def gridsquare(vsk,x,y,w,h,rasterwidth, outline=True):
    dx = 0
    if outline:
        vsk.rectMode("corner")
        vsk.rect(x,y,w,h)
    while dx < w:
        vsk.line(x+dx,y,x+dx,y+h)
        dx+=rasterwidth


def perlingrid(vsk, x, y, w, h, heightvar, noisesize, noisescale=1, seed=1337 ,outline=True):
    # perlingrid(vsk,100,100,600,100,50,2,2,1337, False)
    
    dx = 0
    i = 0
    if outline:
        vsk.rectMode("corner")
        vsk.rect(x,y,w,h)
    while dx < w:
        bh = vsk.noise(dx/10)
        vsk.line(x+dx,y-bh*heightvar,x+dx,y+h+bh*heightvar)
        dx+=(vsk.noise(i)*noisesize)**noisescale
        i+=1




def curveProgression(vsk,w,h,ns):
    '''
    eg:
    for i in range(100):
        curveProgression(vsk,1000,800,100+i/100)
    '''
    x1 = w*vsk.noise(ns+15)
    x2 = w*vsk.noise(ns+25)
    x3 = w*vsk.noise(ns+35)
    x4 = w*vsk.noise(ns+45)
    y1 = h*vsk.noise(ns+55)
    y2 = h*vsk.noise(ns+65)
    y3 = h*vsk.noise(ns+75)
    y4 = h*vsk.noise(ns+85)
    vsk.bezier(x1, y1, x2, y2, x3, y3, x4, y4)
    vsk.bezier(x4, y1, x2, y2, x3, y3, x1, y4)
    vsk.bezier(x2, y1, x2, y2, x3, y3, x1, y4)


def blockline (vsk, x1, y1, x2, y2, subdiv, blockfunc, blockfuncargs):
    rc = (x2-x1)/(y2-y1)
    length = math.sqrt((x2-x1)**2+(y2-y1)**2)
    for i in range(10):
        x = length/10*i*rc
        y = length/10*i/rc
        vsk.rectMode("corner")
        vsk.rect(x,y, 50,50)

def lineflower(vsk, x,y,size,segments,ftype):
    segs = []
    if (ftype == "flower"):
        for i in range(segments):
            segs.append([x,y,x+vsk.random(0,size) - size/2, y+ vsk.random(0, size)-size/2])
    if (ftype == "branch"):
        dx = x
        dy = y
        dirx = random.choice([-1,1])
        diry = random.choice([-1,1])
        for i in range(segments):
            ddx = dx + vsk.random(0,size)*dirx
            ddy = dy + vsk.random(0,size)*diry
            segs.append([dx,dy,ddx,ddy])
            dx=ddx
            dy=ddy

    vsk.pushMatrix()
    for seg in segs:
    # vsk.translate(x,y)
        vsk.line(seg[0],seg[1],seg[2],seg[3])
    vsk.popMatrix()
    
    

def carvegrid(vsk,scale, amount):

    basegrid = [10,6,7,8,10,5,7,8, 3, 5]
    basedir = ["n","e","s","e","n","w","s","w", "s","w","n","w"]

    basegrid = []
    basedir = ["n"]
    dirs = ["n","e","s","w"]
    for i in range(20):
        basegrid.append(int(vsk.random(3,10)))
        basedir.append(dirs[int(vsk.random(0,3))])
    basedir.append("s")
    # print(basegrid)
    # print(basedir)
    for j in range(amount):
        prevdir = "start"
        x = 0
        y = 0
        x+=(1+j)*scale
        for i,l in enumerate(basegrid):
            try: 
                nextdir = basedir[i+1]
            except:
                nextdir = "stop"
            if basedir[i] == "s":
                if (prevdir == 'e'):
                    dx=-j
                    dy=(l-j)
                elif (prevdir == 'w'):
                    dx=0
                    dy=l
                if (nextdir == "e"):
                    dx =0 
                    dy = (l-j)
                prevdir = "n"
            if basedir[i] == "e":
                if (prevdir == 's'):
                    dx = (l+amount-2*j)
                    dy = 0
                elif (prevdir == 'n'):
                    dx = (l-j)
                    dy = 0
                if (nextdir == "n"):
                    dx = (l+j) 
                elif (nextdir == "s"):
                    dx = (l-j) 
                prevdir = "e"
            if basedir[i] == "n":                
                if (prevdir == 'e'):
                    dx = 0
                    dy = (-l)
                elif (prevdir == 'w'):
                    dx = 0
                    dy = (-l)
                else:
                    dx = 0
                    dy = (l-j)
                prevdir = "s"
            if basedir[i] == "w":
                if (prevdir == 's'):
                    dx = -(l+amount-2*j)
                    dy = 0
                elif (prevdir == 'n'):
                    dx = -(l+amount-2*j)
                    dy = 0  
                prevdir = "w"
            dx=dx*scale
            dy=dy*scale                          
            vsk.line(x,y,x+dx,y+dy)
            x+=dx
            y+=dy

def disintegrationSquare(vsk,x,y,w,h,space, disfactor):
    dx = x
    while (dx < w):
        dh = y
        while (dh < h):
            H = vsk.random(h/disfactor)
            vsk.line(dx,dh,dx,dh+H)
            H = vsk.random(h/disfactor)
            dh+=H

        dx+=space   

def lixelblock(vsk, lixelsize, xs, ys, ortho=True, lixelchance=0):
    for i in range(xs):
        for j in range(ys):
            # vsk.rect(lixelsize*1.1*i,lixelsize*1.1*j,lixelsize,lixelsize)
            x = lixelsize*1.1*i
            y = lixelsize*1.1*j
            x1=x   
            y1=y             
            for t in range (j):
                if ortho:
                    if (t%2==0):
                        x2=x1
                        y2=y+vsk.random(0,lixelsize)
                    else:
                        y2=y1
                        x2=x+vsk.random(0,lixelsize)
                else:
                    x2=x+vsk.random(0,lixelsize)
                    y2=y+vsk.random(0,lixelsize)
                if random.random() > lixelchance:
                    vsk.line(x1,y1,x2,y2)
                x1=x2
                y1=y2
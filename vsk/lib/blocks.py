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
    
    

def sinegrid(vsk, x, y, w, h, sinesize, scale ,outline=True):
    dx = 0
    i = 0
    if outline:
        vsk.rectMode("corner")
        vsk.rect(x,y,w,h)
    while dx < w:
        dr = random.randint(0,scale)*scale
        vsk.line(x+dx,y-dr,x+dx,y+h+dr)
        if math.sin(math.radians(i))*sinesize == 0:
            sine = 0.1
        else:
            sine = math.sin(math.radians(i))*sinesize
        print(dx, sine)
        dx+=abs(sine)**scale
        i+=1

def brokenrotatedcircle (vsk,x,y, num, decay, segs, size):
    s = 2*math.pi/segs
    for i in range(num):
        # c = shapes.group([])
        d = vsk.random(1,int(segs/20)+2)
        e = 0
        while e < segs:
            g = random.randint(0,int(segs/d))
            # seg = shapes.arc_circle(size*math.pow(decay,i), s*e, s*(e+g), segs, '2PI')
            vsk.arc(2, 3, 5, 4, 0, np.pi / 2)
            e = e + g + g/2
            # c.append(seg)
        vsk.pushMatrix()
        # transforms.rotate(c, math.degrees(360/segs/num*i))
        # transforms.offset(c, (x+random.randint(0,int(size/20)),y+random.randint(0,int(size/20))))
        vsk.popMatrix()


def carvegrid(vsk,scale, amount):

    basegrid = [10,6,7,8,10,5,7,8, 3, 5]
    basedir = ["n","e","s","e","n","w","s","w", "s","w","n","w"]

    basegrid = []
    basedir = ["n"]
    dirs = ["n","e","s","w"]
    for i in range(10):
        basegrid.append(int(vsk.random(3,5)))
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


def conradsquares(vsk, x,y,amount,xsize, ysize, error, chance):
    for i in range(amount):
        r = random.random()
        if r > chance:
            x1=x+(error/2 - random.random()*error)
            y1=y+(error/2 - random.random()*error)
            x2=x+(error/2 - random.random()*error)+xsize
            y2=y+(error/2 - random.random()*error)
            x3=x+(error/2 - random.random()*error)+xsize
            y3=y+(error/2 - random.random()*error)+ysize
            x4=x+(error/2 - random.random()*error)
            y4=y+(error/2 - random.random()*error)+ysize
            vsk.line(x1,y1,x2,y2)
            vsk.line(x2,y2,x3,y3)
            vsk.line(x3,y3,x4,y4)
            vsk.line(x4,y4,x1,y1)

def conradquads(vsk, x,y,amount,xsize, ysize, error, chance):
    for i in range(amount):
        r = random.random()
        if r > chance:
            x1=x+(error/2 - random.random()*error)
            y1=y+(error/2 - random.random()*error)
            x2=x+(error/2 - random.random()*error)+xsize
            y2=y+(error/2 - random.random()*error)
            x3=x+(error/2 - random.random()*error)+xsize
            y3=y+(error/2 - random.random()*error)+ysize
            x4=x+(error/2 - random.random()*error)
            y4=y+(error/2 - random.random()*error)+ysize
            # vsk.rotate(random.random())
            vsk.fill(1)
            vsk.quad(x1,y1,x2,y2,x3,y3,x4,y4)
            vsk.noFill()
            vsk.quad(x1,
                     y1,
                     x2,
                     y2,
                     x2+random.random()*ysize,
                     y2-random.random()*ysize,
                     x1+random.random()*xsize,
                     y1-random.random()*ysize) 
 

def conradshape(vsk, shapescale, jitter, xscale, yscale):
    p1=[3,1]
    p2=[5,1]
    p3=[2,1]
    p4=[7,1]
    p5=[3,2]
    p6=[4,2]
    p7=[5,2]
    p8=[6,3]
    p9=[7,3]
    p10=[7,3]
    p11=[1,2]
    p12=[1,3]
    p13=[3,3]
    p14=[3,4]
    p15=[5,3]
    p16=[6,4]
    p17=[7,5]
    p18=[7,5]
    p19=[1,3]
    p20=[4,4]
    p21=[5,4]
    p22=[6,5]
    p23=[1,5]
    p24=[1,4]
    p = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23]
    for point in p:
        # print(p)
        point[0]=point[0]+random.random()*jitter*xscale
        point[1]=point[1]+random.random()*jitter*yscale
        print(p)
    shapes = [[p3,p5,p11],
                [p3,p1,p6,p5],
                [p2,p7,p6], 
                [p2,p4,p8,p7],
                [p4,p8,p9],
                [p8,p9,p10,p15],
                [p7,p8,p15],
                [p6,p7,p14],
                [p5,p6,p14,p13],
                [p11,p5,p13,p12],
                [p19,p13,p20,p24],
                [p13,p14,p21,p20],
                [p14,p7,p15,p21],
                [p15,p10,p16,p21],
                [p16,p10,p18,p17],
                [p16,p17,p21],
                [p20,p21,p17,p22],
                [p24,p20,p22,p23]
                ]     
    vsk.pushMatrix()
    vsk.scale(shapescale)
    for shape in shapes:
        if (len(shape) == 4):
            x1 = shape[0][0]
            y1 = shape[0][1]
            x2 = shape[1][0]
            y2 = shape[1][1]
            x3 = shape[2][0]
            y3 = shape[2][1]
            x4 = shape[3][0]
            y4 = shape[3][1]
            if (random.random()>0.8):
                vsk.fill(1)
            else:
                vsk.noFill()
            vsk.quad(x1,y1,x2,y2,x3,y3,x4,y4)

        if (len(shape) == 3):
            x1 = shape[0][0]
            y1 = shape[0][1]
            x2 = shape[1][0]
            y2 = shape[1][1]
            x3 = shape[2][0]
            y3 = shape[2][1]
            if (random.random()>0.8):
                vsk.fill(1)
            else:
                vsk.noFill()
            vsk.triangle(x1,y1,x2,y2,x3,y3)
    vsk.popMatrix()


def conradshape2(vsk, shapescale, jitter, xscale, yscale):
    p1=[1,1]
    p2=[1,5]
    p3=[1,7]
    p4=[1,9]
    p5=[2,5]
    p6=[2,7]
    p7=[2,1.5]
    p8=[3.25,5]
    p9=[4,7]
    p10=[5,10]
    p11=[3,1.25]
    p12=[3,2]
    p13=[4,5]
    p14=[5,7]
    p15=[6,10.25]
    p16=[4,1.25]
    p17=[7,10.5]
    p18=[5,1]
    p19=[8,11]

    p = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19]
    for point in p:
        # print(p)
        point[0]=point[0]+random.random()*jitter*xscale
        point[1]=point[1]+random.random()*jitter*yscale
        print(p)
    shapes = [[p1,p7,p8,p5,p2,p1],
                [p7,p11,p12,p13,p8,p7],
                [p12,p16,p17,p15,p14,p9,p6,p5,p8,p13,p12], 
                [p16,p18,p19,p17,p16],
                [p9,p14,p15,p10,p9],
                [p3,p6,p9,p10,p4,p3]
                ]     
    vsk.pushMatrix()
    vsk.scale(shapescale)
    for shape in shapes:
        shapearray = []
        for point in shape:
            shapearray.append((point[0],point[1]))
        if (random.random()>0.9):
            vsk.fill(1)
        else:
            vsk.noFill()
        
        vsk.polygon(shapearray)


    vsk.popMatrix()


def conradshape3(vsk,shapescale,jitter,size,xscale,yscale):
    points = []
    for s in range(size):
        points.append((random.random()*xscale, random.random()*yscale))
    shapes = []
    for i in range(int(size/3)+1):
        # for x in range(3):
        if (random.random() > 0.9):
            vsk.fill(1)
        shapes.append(random.choice(points)) 
        # shapes.
    
    # for j in range(len(shapes)):
        # print(shapes)
    vsk.polygon(shapes)

    # print(shapes)    
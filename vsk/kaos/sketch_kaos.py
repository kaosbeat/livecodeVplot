import vsketch
import math
import random
import numpy as np
from lib.blocks import *

class KaosSketch(vsketch.SketchClass):
    # Sketch parameters:
    radius = vsketch.Param(59.0)
    size = vsketch.Param(40.0)
    W = vsketch.Param(14)
    H = vsketch.Param(20)
    noiselod = vsketch.Param(1) 
    papersize = "749mmx1759mm"


    def draw(self, vsk: vsketch.Vsketch) -> None:
        # vsk.size("a3", landscape=False)
        vsk.scale("mm") 
        vsk.size(self.papersize, landscape=False, center=False)
        vsk.rectMode("corner")
        vsk.pushMatrix() 
        # vsk.translate(100,100)
        vsk.penWidth("0.3mm")
        # vsk.fill(1)
        subdivpattern(vsk,180,1030,150,650,3,1)

        vsk.translate(350,1100)
        for x in range(5):
            for y in range(8):
                cscale = 20
                vsk.pushMatrix()
                vsk.scale(1.52)
                # vsk.rotate(90, True)
                vsk.translate(x*cscale, y*cscale)
                if (random.random()>0.3):
                    vsk.scale(1.6)
                    # conradshape3(vsk,1000, 12,13, 30, 30)
                vsk.popMatrix()
        # for i in range(10):
        #     for j in range(5):
        # vsk.translate(420, 1760-520)
        # vsk.rotate(23,True)
        # vsk.rect(60,80,vsk.random(50,80),vsk.random(50,80))
        # vsk.rect(160,80,100,20)
        # for i in range(10):
        #     for j in range(25):
        #         if (random.random() > 0.5):
        #             vsk.rect(100 +20*i,100 -10*j,10,20)
        
        vsk.translate(100, 420)
        for x in range(6):
            vsk.rotate(-15,True)
            # vsk.rect(0-+random.random()*40,35*x,350+random.random()*40,30 )
        # carvegrid(vsk,2,40)
        # vsk.rotate(90, True)
        # vsk.translate(200,-350)
        # vsk.scale(0.5)
        # carvegrid(vsk,4,40)
        vsk.translate(-330,-510)
        vsk.scale(1,-1)
        # vsk.rotate(90, True)
        # vsk.line(200,500,450,600)
        # vsk.rect(10,0,50,50)
        # vsk.rect(600,0,50,250)
        # vsk.rect(0,1500,150,50)
        # vsk.rect(600,1500,150,150)
        # vsk.penWidth("0.5mm")
        # vsk.fill(1)
        # perlingrid(vsk,100,100,600,100,50,2,2,1337, False)
        # vsk.rotate(-80, True)
        # vsk.translate(-910,270)
        # vsk.rotate(180,True)
        # vsk.translate(-1000,-300)
        # for i in range(10):
        #     vsk.line(0,0,100,i*10)
        #     for j in range(50):
        #         vsk.line(110, 60*i, j*20,5*j)
        # disintegrationSquare(vsk, 10,10,50,580,3,3)
        # vsk.rotate(90, True)

        # vsk.rotate(90, True)
        # vsk.translate(600,-450)
        # vsk.rotate(90,True)
        vsk.scale(0.6)
        # # vsk.translate(-210,-245)

        # carvegrid(vsk,4,38)
        # carvegrid(vsk,4,3)
        # carvegrid(vsk,4,38)
        # # vsk.translate(-60,45)
        # # vsk.rotate(45, True)

        # # carvegrid(vsk,2,45)
        # vsk.rotate(-45, True)

        # vsk.translate(-60,45)
        # # carvegrid(vsk,2,3)

        # # disintegrationSquare(vsk, 20,-40,150,180,2,1)
        # vsk.rotate(180, True)
        # vsk.translate(-181,-200)
        # disintegrationSquare(vsk, 20,-40,150,180,2,1)
        
        # sinegrid(vsk,162,130,400,100,3,4, False)
        # sinegrid(vsk,142,180,600,40,2,4, False)
        # sinegrid(vsk,152,20,300,100,2,4, False)
    

        # vsk.rotate(180, True)
        # vsk.translate(-181,-200)
        # for r in range(10):
        #     vsk.arc()       
        # sinegrid(vsk,162,130,400,100,3,4, False)
        # sinegrid(vsk,142,180,600,40,2,4, False)
        # sinegrid(vsk,152,20,300,100,2,4, False)
    
        # brokenrotatedcircle (vsk,10, 20, 4, 20, 30, 30)

        # vsk.text("topleft", 100, 200)
        # vsk.rect(10,0,50,50)
        # vsk.rect(600,0,50,250)
        # vsk.rect(0,1500,150,50)
        # vsk.rect(600,1500,150,150)
        # # vsk.text("bottomright", 600, 1500)
        vsk.translate(1100,-1400)
        vsk.rotate(-50,True)

        # vsk.scale(0.5)
        # carvegrid(vsk,4,40)
        vsk.translate(-250,-300)
        vsk.rotate(-30,True)

        # carvegrid(vsk,2,24)
        vsk.translate(50,-750)
        # carvegrid(vsk,2,24)


        # vsk.translate(0,1300)

        # sinegrid(vsk,162,130,400,100,3,4, False)
        # sinegrid(vsk,182,10,160,160,2,4, False)
        # sinegrid(vsk,162,10,60,40,2,4, False)
        # sinegrid(vsk,152,20,300,100,2,4, False)

        # self.circlegrid(vsk)                           
        # self.squaresgrid(vsk)
        # filledSquares(vsk, 10, 250, 300, 20)
        # stackSquares(vsk, 10, 205, 10, 100)
        # blockline (vsk, 100, 10, 10, -20, 10, 1, 1)

        # vsk.rotate(100,True )
        
        # lixelblock(vsk,10,3,40, True)
        # vsk.rotate(140,True)
        # vsk.translate(110,400)
        # lixelblock(vsk,10,3,40, True)
        # lixelblock(vsk,22,30,20, True, 0.4)
        vsk.scale(1)
        vsk.translate(-1300,500)
        # for x in range(4):
        #     for y in range(5):
        # #         # conradsquares(vsk, x*100,y*100,8,random.random()*30+y*20, random.random()*x/20+80 ,40, y/8 )
        # #         # vsk.fill(1)
        #         conradquads(vsk, x*100,y*100,1,random.random()*30+y*20, random.random()*x/20+80 ,40, y/8 )
        
        
        vsk.popMatrix()

        x=100
        y=100
        vsk.pushMatrix()
        vsk.translate(405,178)
        vsk.rotate(20,True)
        vsk.scale(0.5)
        for i in range(10):
            # curveProgression(vsk,1000,800,100+i/100)
            for j in range(30):
                x = i*15
                y = j*10
                # curveProgression(vsk,400,100,x/1000)
                # vsk.line(x,y,(i+1)*50, (j+1)*100)
                # lineflower(vsk, x, y,30,j,"branch")
        # self.blocks(vsk, 100, 100, 200, 20)
        self.finalize(vsk) 
                
    def finalize(self, vsk: vsketch.Vsketch) -> None:
        # vsk.vpype("linemerge linesimplify reloop linesort")
        # vsk.save("squares.hpgl", "dxy", paper_size="a3")
        vsk.save("blocks.svg", paper_size=self.papersize)

    def circlegrid(self, vsk):
        # # Sketch parameters:
        # radius = vsketch.Param(1.0)
        # size = vsketch.Param(1.0)
        # W = vsketch.Param(20)
        # H = vsketch.Param(20)
        # noiselod = vsketch.Param(1)
        vsk.noiseDetail(self.noiselod)
        vsk.stroke(1)
        for w in range(self.W):
            for h in range(self.H):
                vsk.circle(w*self.size, h*self.size, self.radius*vsk.noise(w,h), mode="radius")
        vsk.stroke(1)
        vsk.noiseSeed(2)
        for w in range(self.W):
            for h in range(self.H):
                vsk.circle(w*self.size, h*self.size, self.radius*vsk.noise(w,h), mode="radius")
        vsk.stroke(1)
        vsk.noiseSeed(3)
        for w in range(self.W):
            for h in range(self.H):
                vsk.circle(w*self.size, h*self.size, self.radius*vsk.noise(w,h), mode="radius")
                
    # def squaresgrid(self, vsk):
    #     done = False
    #     totalsizeX=297
    #     totalsizeY=420
    #     totalX = totalsizeX
    #     totalY = totalsizeY
    #     vsk.stroke(1)
    #     subdivpattern(vsk,0,0,250,250,3,1)
    #     vsk.stroke(1)
    #     subdivpattern(vsk,0,0,250,250,3,1)


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




if __name__ == "__main__":
    KaosSketch.display()


# plotter.write(fillsquare(5000,300,1000,1000,90,80,1))

import vsketch
import math
import random
from lib.blocks import *

class KaosSketch(vsketch.SketchClass):
    # Sketch parameters:
    radius = vsketch.Param(59.0)
    size = vsketch.Param(40.0)
    W = vsketch.Param(14)
    H = vsketch.Param(20)
    noiselod = vsketch.Param(1) 
    papersize = "750mmx1780mm"

    def draw(self, vsk: vsketch.Vsketch) -> None:
        # vsk.size("a3", landscape=False)
        vsk.scale("mm") 

        vsk.size(self.papersize, landscape=False, center=False)
        vsk.rectMode("corner")
        vsk.pushMatrix() 
        vsk.translate(0,0)
        vsk.penWidth("0.5mm")
        # vsk.fill(1)
        # vsk.rect(100,200,50,50)

        # subdivpattern(vsk,20,1230,250,250,3,1)
        # vsk.rect(10,0,50,50)
        # vsk.rect(600,0,50,250)
        # vsk.rect(0,1500,150,50)
        # vsk.rect(600,1500,150,150)
        # self.circlegrid(vsk)                           
        # self.squaresgrid(vsk)
        # filledSquares(vsk, 10, 250, 300, 20)
        # stackSquares(vsk, 10, 205, 10, 100)
        # blockline (vsk, 100, 10, 10, -20, 10, 1, 1)
        # vsk.translate(100,400)
        x=100
        y=100
        for i in range(10):
            for j in range(20):
                x = i*50
                y = j*100
                vsk.line(x,y,(i+1)*50, (j+1)*100)
                lineflower(vsk, x, y,10,j,"branch")
        # self.blocks(vsk, 100, 100, 200, 20)
        vsk.popMatrix()
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



if __name__ == "__main__":
    KaosSketch.display()

def fillsquare(vsk, xoffset,yoffset,width,height,angle,interval,outline):
    if (outline == 1):
        vsk.rect(xoffset,yoffset,width,height)
    for x in range(int(width/interval)):
        vsk.line(xoffset+x*interval,yoffset+0,xoffset+x*interval,yoffset+height )

# plotter.write(fillsquare(5000,300,1000,1000,90,80,1))

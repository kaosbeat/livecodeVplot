import vsketch
import math
from lib.blocks import *

class KaosSketch(vsketch.SketchClass):
    # Sketch parameters:
    radius = vsketch.Param(59.0)
    size = vsketch.Param(40.0)
    W = vsketch.Param(14)
    H = vsketch.Param(20)
    noiselod = vsketch.Param(1) 
    papersize = "790mmx1720mm"

    def draw(self, vsk: vsketch.Vsketch) -> None:
        # vsk.size("a3", landscape=False)
        vsk.scale("mm") 

        vsk.size(self.papersize, landscape=False, center=False)
        vsk.rectMode("corner")
        vsk.pushMatrix() 
        vsk.translate(0,0)
        vsk.penWidth("0.5mm")
        vsk.fill(1)
        vsk.rect(100,200,50,50)
        # vsk.rect(10,0,50,50)
        vsk.rect(600,0,50,250)
        vsk.rect(0,1500,150,50)
        vsk.rect(600,1500,150,150)
        # self.circlegrid(vsk)                           
        # self.squaresgrid(vsk)
        # filledSquares(vsk, 10, 250, 300, 20)
        # stackSquares(vsk, 10, 205, 10, 100)
        # blockline (vsk, 100, 10, 10, 2000, 3, 1, 1)
        
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



if __name__ == "__main__":
    KaosSketch.display()

def fillsquare(vsk, xoffset,yoffset,width,height,angle,interval,outline):
    if (outline == 1):
        vsk.rect(xoffset,yoffset,width,height)
    for x in range(int(width/interval)):
        vsk.line(xoffset+x*interval,yoffset+0,xoffset+x*interval,yoffset+height )

# plotter.write(fillsquare(5000,300,1000,1000,90,80,1))


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
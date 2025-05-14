import vsketch
import math
import numpy as np

class TestvskSketch(vsketch.SketchClass):
    # Sketch parameters:
    columns = vsketch.Param(12)
    rows = vsketch.Param(22)
    fuzziness = vsketch.Param(1.0)
    size = vsketch.Param(12)
    interx =vsketch.Param(12) 
    intery = vsketch.Param(12) 
    xnoise = vsketch.Param(12) 
    ynoise = vsketch.Param(12)
    N = vsketch.Param(200, 0)
    freq = vsketch.Param(0.003, decimals=3)
    drift = vsketch.Param(0.06, decimals=2)
    # radius = vsketch.Param(2.0)



# def draw(size, seed, interx, intery, xnoise, ynoise):
    def draw(self, vsk: vsketch.Vsketch) -> None:
        # self.petals(vsk)
        # vsk.stroke(2)
        # self.noiselines(vsk)
        self.squarestudy(vsk)
    
    def jsq(self, depth, size):   
        jsquare = self.vsk.createShape()
        x=0
        y=0
        dx=0
        dy=0
        for i in range(depth):
            h = self.vsk.random(0,2)
            v = self.vsk.random(0,2)
            if h > 1:
                dx = self.vsk.random(0,size)
            if v < 1:
                dy = self.vsk.random(0,size) 
            self.vsk.line(x,y,dx,dy)
            x=dx
            y=dy
        return jsquare 
        
    def squarestudy(self, vsk: vsketch.Vsketch):
        print("squarestudy")
        size = self.size        
        for w in range(1):
            for h in range(12):
                shape = self.jsq(w+h, size)
                vsk.stroke(1)
                vsk.fill(2)
                vsk.shape(shape)


    def petals(self, vsk: vsketch.Vsketch):
        for x in range(0,self.size):
            points = []
            normx = (x-(self.size/2))/float(self.size/2)
            xnoise = self.xnoise + self.size/50
            ynoise = self.ynoise + self.size/50
            print(normx)
            for y in range(0,self.size):          
                yoff = math.cos(math.asin(normx))*self.size/2
                ybuf = (self.size/2 - yoff)
                if ((y < ybuf ) or y > self.size-ybuf) :
                    xn = 0
                    yn = 0
                else:
                    xn = xnoise
                    yn = ynoise

                xpos = x*self.interx + vsk.random(10) * xn
                ypos = y*self.intery + vsk.random(10) * yn
                # if (x == 12):
                #     print(y, size*0.1)
                #     print(xpos,ypos, ynoise)
                points.append((xpos,ypos))
                
            t = np.arange(self.N) * self.freq
            perlin = vsk.noise(t, np.arange(8) * 1000)
            for i in range(len(points)-1):
                v = i * self.drift
                if i % 2 == 0:
                    k = -1
                else:
                    k = 1
                vsk.bezier(points[i][0],points[i][1],
                              points[i][0] + k*xnoise ,
                              points[i][1],
                              points[i+1][0] + k*xnoise,
                              points[i+1][1],
                            
                            # perlin[i, 2] * 1000 + v,
                            # perlin[i, 3] * 1000 + v,
                            # perlin[i, 4] * 1000 + v,
                            # perlin[i, 5] * 1000+ v,
                            points[i+1][0],points[i+1][1])
                        # vsk.line(points[i][0],points[i][1], points[i+1][0],points[i+1][1])
 
    def noiselines(self, vsk: vsketch.Vsketch):
            for x in range(0,self.size):
                points = []
                normx = (x-(self.size/2))/float(self.size/2)
                xnoise = self.xnoise + self.size/50
                ynoise = self.ynoise + self.size/50
                print(normx)
                for y in range(0,self.size):          
                    yoff = math.cos(math.asin(normx))*self.size/2
                    ybuf = (self.size/2 - yoff)
                    if ((y < ybuf ) or y > self.size-ybuf) :
                        xn = 0
                        yn = 0
                    else:
                        xn = xnoise
                        yn = ynoise

                    xpos = x*self.interx + vsk.random(10) * xn
                    ypos = y*self.intery + vsk.random(10) * yn
                    # if (x == 12):
                    #     print(y, size*0.1)
                    #     print(xpos,ypos, ynoise)
                    points.append((xpos,ypos))
                for i in range(len(points)-1):
                    vsk.line(points[i][0],points[i][1], points[i+1][0],points[i+1][1])

    
    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")

if __name__ == "__main__":
    TestvskSketch.display()


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


def lineflower(x,y,size,segments,ftype):
    segs = []
    if (ftype == "flower"):
        for i in range(segments):
            segs.append([x,y,vsk.random(0.5*size, size), vsk.random(0.5,size)])

    vsk.pushMatrix()
    for seg in segs:
    # vsk.translate(x,y)
        vsk.line(seg[0],seg[1],seg[2],seg[3])
    vsk.popMatrix()
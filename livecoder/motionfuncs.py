import math

### vector function




def dist(x1,y1,x2,y2):
    print(x1,y1,x2,y2)
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    print (dist)
    return dist
    


## motion functions

# X = distance
# A = acceleration
# T = time
# V = velocity.


## linear motion

def XfromVT(v,t):
    x = v*t
    return x

def VfromXT(x,t):
    v = x/t
    return v

def Tfrom(x,v):
    t = x/v
    return t



### accelerated motion

def XfromAT(a,t):
    x = (a*t**2)/2
    return x

def XfromVA(v,a):
    x = (v**2)/(2*a)
    return x

def VfromAT(a,t):
    v = a*t
    return v

def VfromXA(x,a):
    v = math.sqrt(2*a*x)
    return v

def AfromVT(v,t):    
    a = v/t
    return a

def AfromXT(x,t):
    a = (2*x)/t**2
    return a

def AfromVX(v,x):
    a = v**2/(2*x)
    return a

def TfromVA(v,a):
    t = v/a
    return t

def TfromXA(x,a):
    t = math.sqrt((2*x)/a)
    return t



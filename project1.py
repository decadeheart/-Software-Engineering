import random
INF = 1e9
T = 100            #Starting temperature
delta = 0.9        #Temperature dropping rate
THRESHOLD = 1e-6   #Threshold value
MOVE = 100         #Times of comparing for centers
PREOPT = 1e-6      #Least radius accuracy
alpha = 0.2        #Learning rate
MINEX = 1e-1       #Solvability condition

dx = [ 0, 0, -1, 1 ]
dy = [ 1, -1, 0, 0 ]  #Up, down, left, right


class Circle:
    def __init__(self):
        self.radius = 0
        self.x = 0
        self.y = 0


def initialize(n):
    cir = [Circle()]*n
    for i in range(n):
        cir[i].radius = 0
        cir[i].x = 0
        cir[i].y = 0
    return cir

def dist(A,B):#Dis of A,B's centers
    return ((A.x - B.x)**2+(A.y - B.y)**2)**(1/2)

def Getsum(cir,n,c):
    ans = 0
    for i in range(n):
        ans += (cir[i].radius + c.radius - dist(cir[i], c))**2
    if (c.x + c.radius > 1):
        ans += (c.x + c.radius - 1)**2
    if (c.x - c.radius < -1):
        ans += (c.x - c.radius + 1)**2
    if (c.y + c.radius > 1):
        ans += (c.y + c.radius - 1)**2
    if (c.y - c.radius < -1):
        ans += (c.y - c.radius + 1)**2
    return ans

def GetCenter(cir,n):
    c=Circle()
    flag = 0
    c.radius = 0
    #Center£¨x,y£© in [£­1£¬1],tentative randomly
    c.x = 2 * random.random() - 1
    c.y = 2 * random.random() - 1
    while (flag < n):
        c.x = 2 * random.random() - 1
        c.y = 2 * random.random() - 1
        flag = 0
        for i in range(n):
            if (dist(cir[i], c) > cir[i].radius):
                flag+=1
            else:
                break
    return c

def GetCircle(cir,n,curradius):
    MinCir=Circle()
    MinEx = INF
    MinCir.radius = 0
    MinCir.x = 0
    MinCir.y = 0
    #gradient descent
    k=0
    while (k < MOVE):
        c = GetCenter(cir, n)
        c.radius = curradius
        Ex = Getsum(cir, n, c)
        if (Ex < MinEx):
            MinCir = c
            MinEx = Ex
        k+=1
    return MinCir

def optimize(cir,n):
    x1 = cir[n - 1].x
    y1 = cir[n - 1].y
    ax = 0
    ay = 0
    for i in range(n):
        j=i+1
        while(j < n):
            ax -= 2 * (cir[i].radius + cir[j].radius - dist(cir[i], cir[j])**0.5) * dist(cir[i], cir[j])**(-0.5) * (x1 - cir[j].x)
            ay -= 2 * (cir[i].radius + cir[j].radius - dist(cir[i], cir[j])**0.5) * dist(cir[i], cir[j])**(-0.5) * (y1 - cir[j].y)
            j+=1
        if (cir[i].x + cir[i].radius > 1):
            ax += 2 * (cir[i].x + cir[i].radius - 1)
        if (cir[i].x - cir[i].radius < -1):
            ax += 2 * (cir[i].x - cir[i].radius + 1)
        if (cir[i].y + cir[i].radius > 1):
            ay += 2 * (cir[i].y + cir[i].radius - 1)
        if (cir[i].y - cir[i].radius < -1):
            ay += 2 * (cir[i].y - cir[i].radius + 1)
    x2 = x1 - alpha * ax
    y2 = y1 - alpha * ay
    cir[n - 1].x = x2
    cir[n - 1].y = y2
    return cir[n - 1]

def Search(cir,n):
    ans=0
    t = T
    flag = [0] * n
    while (t > THRESHOLD):
        for i in range(n):
            curradius = PREOPT#The Smallest radius
            if (flag[i] == 1):
                continue
            c = GetCircle(cir,i, curradius)#The ith circle
            #Optimize gradient descent
            cir[i] = c
            c = optimize(cir, i + 1)
            while (Getsum(cir, i, c) < MINEX / n):
                #print "curradius = ",curradius
                curradius *= 1.1
                c = GetCircle(cir, i, curradius)
                cir[i] = c
                c = optimize(cir, i + 1)
                if (Getsum(cir, i, c) > MINEX / n):
                    k=0
                    while (k < 10 and Getsum(cir, i, c) > MINEX / n):
                        c = GetCircle(cir, i, curradius)
                        cir[i] = c
                        c = optimize(cir, i + 1)
                        k+=1
            c.radius = curradius / 1.21
            cir[i] = c
            flag[i] = 1
            ans += Getsum(cir, i, c)
        if (ans < MINEX):
            return ans
        else:
            t = t*delta
    return ans

def main():
    while (1):
        #input
        print "Please enter the number of circles:"
        num = input()
        if (num > 0):
            #Initialize circles
            cir = initialize(num)
            #find the position and radius
            ans = Search(cir, num)
            if (ans == -1):
                print "There is no answer, please try again"
            else:
                for i in range(num):#output for each
                    print cir[i].radius , cir[i].x , cir[i].y
                #total area
                #print ans
        else:
            break

main()

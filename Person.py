from random import randint
import time

class MyPerson:
    tracks = []
    def __init__(self, i, xi, yi, max_age):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None
        self.linija1 = None
        self.linija2 = None
        self.dingimas=0
    def getRGB(self):
        return (self.R,self.G,self.B)
    def getTracks(self):
        return self.tracks
    def getDingimas(self):
        return self.dingimas
    def updateDingimas(self, x):
        self.dingimas=x
    def getId(self):
        return self.i
    def getState(self):
        return self.state
    def getDir(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x,self.y])
        self.x = xn
        self.y = yn
    def setDone(self):
        self.done = True
    def timedOut(self):
        return self.done
    def going_UP(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[1][1] > mid_end and self.tracks[-2][1] <= mid_start: #cruzo la linea
                    self.state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False
    def going_DOWN(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[1][1] < mid_start and self.tracks[-2][1] >= mid_end: #cruzo la linea
                    self.state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False
        
##Donato kodas
    def cross_bottom(self, bottom_line):
        if self.tracks[0][1] < bottom_line < self.tracks[-1][1]: #ar kirto linija is apacios
            if self.linija1 != 'top':
                self.linija1 = 'bottom'
            else: self.linija2 = 'bottom'
        if self.tracks[0][1] > bottom_line > self.tracks[-1][1]: ##ar kirto linija is virsaus
            if self.linija1!='top':
                self.linija1 = 'bottom'
            else: self.linija2 = 'bottom'
                

    def cross_top(self, top_line):
        if self.tracks[0][1] < top_line < self.tracks[-1][1]: #ar kirto linija is apacios
            if self.linija1!='bottom':
                self.linija1 = 'top'
            else: self.linija2 = 'top'
        if self.tracks[0][1] > top_line > self.tracks[-1][1]: ##ar kirto linija is virsaus
            if self.linija1!='bottom':
                self.linija1 = 'top'
            else: self.linija2 = 'top'        
            
    def kurEina(self,bottom_line,top_line):
        if len(self.tracks) >= 2:
            if self.dir == None:
                self.cross_bottom(bottom_line)
                self.cross_top(top_line)
                if  self.linija1== 'top' and self.linija2== 'bottom':
                    self.dir = 'down'
                elif  self.linija1== 'bottom' and self.linija2== 'top':
                    self.dir = 'up'
        else:
            return False
        
    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True
    
class MultiPerson:
    def __init__(self, persons, xi, yi):
        self.persons = persons
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        

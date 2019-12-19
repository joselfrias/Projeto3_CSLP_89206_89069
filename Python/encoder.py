from PIL import Image
import numpy as np
from Golomb import Golomb
from BitStream import Stream
import time

class Encoder:
    def __init__(self, filename,mode):
        self.filename=filename
        self.mode=mode
        self.width=720
        self.height=1280
        self.frame_len=0
        self.bStream = Stream()
        self.gol = Golomb(4)
        self.totalTime = 0


    def showImage(self):
        f=open(self.filename, "rb")
        frame=f.readline().decode('utf-8')
        rgb = np.zeros((self.width, self.height,3),dtype=np.uint8)
        if self.mode == '4:4:4':
            self.frame_len=self.width*self.height*3
            raw = f.read(self.frame_len)
            y = np.frombuffer(raw, dtype=np.uint8, count=self.width*self.height)
            u= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height)
            v= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height*2)
            y = y.reshape(self.width,self.height)
            u=u.reshape(self.width,self.height)
            v=v.reshape(self.width,self.height)
            for i in range(0, self.width):
                for j in range(0, self.height):
                    rgb[i][j]=[y[i][j]+1.403*(v[i][j]-128),y[i][j]-0.714*(v[i][j]-128)-0.344*(u[i][j]-128),y[i][j]+1.773*(u[i][j]-128)]
            img = Image.fromarray(rgb, 'RGB')
            img.show()

    def showEncodedImage(self):
        yMatrix = np.zeros((self.width, self.height), dtype=np.uint8)
        uMatrix = np.zeros((self.width,self.height), dtype=np.uint8)
        vMatrix = np.zeros((self.width,self.height), dtype=np.uint8)
        tim = time.time()
        file = open('timeOut.txt', 'rb')
        yMatrix = self.readData(yMatrix, '1', file)
        uMatrix = self.readData(uMatrix, '1', file)
        vMatrix = self.readData(vMatrix, '1', file)
        rgb=np.zeros((self.width, self.height,3),dtype=np.uint8)
        yMatrix=yMatrix.reshape(self.width,self.height)
        uMatrix=uMatrix.reshape(self.width,self.height)
        vMatrix=vMatrix.reshape(self.width,self.height)
        for i in range(0, self.width):
            for j in range(0, self.height):
                rgb[i][j] = [yMatrix[i][j]+1.403*(vMatrix[i][j]-128),yMatrix[i][j]-0.714*(vMatrix[i][j]-128)-0.344*(uMatrix[i][j]-128),yMatrix[i][j]+1.773*(uMatrix[i][j]-128)]
        img = Image.fromarray(rgb, 'RGB')
        img.show()
        file.close()

    def readData(self, matrix, predictorType, file):
        for i in range(0, self.width):
            for j in range(0, self.height):
                y = []
                while True:
                    nBit = self.bStream.readbits(1, file)
                    y.append(nBit)
                    if nBit == 0:
                        for c in range(0, 2):
                            y.append(self.bStream.readbits(1, file))
                        break
                #print(y)
                dec = self.gol.decode(y)
                if dec%2 == 0:
                    e = dec/2
                else:
                    e = -1*((dec+1)/2)
                p = int(self.predictor(matrix, i, j, '1'))
                x = int(e + p)
                matrix[i][j] = x
                #time.sleep(1)
        return matrix

    def realSpace(self):
        f=open(self.filename, "rb")
        nFrame = 0
        #read header with info of the video
        frame=f.readline().decode('utf-8')
        #Maybe read size of the images
        rgb=np.zeros((self.width,self.height,3), dtype=np.uint8)
        if self.mode=='4:4:4':
                    self.frame_len=self.width*self.height*3
                    x=f.readline() # read word Frame
                    raw = f.read(self.frame_len)
                #try:
                    y = np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height)
                    u= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height)
                    v= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height*2)
                    y = y.reshape(self.width,self.height)
                    u=u.reshape(self.width,self.height)
                    v=v.reshape(self.width,self.height)
                    self.bStream.setMatrix('y')
                    for i in range(0, self.width):
                        for j in range(0, self.height):
                            self.bStream.writeBits(y[i][j], 1)
                    self.bStream.setMatrix('u')
                    for i in range(0, self.width):
                        for j in range(0, self.height):
                            self.bStream.writeBits(u[i][j], 1)
                    self.bStream.setMatrix('v')
                    for i in range(0, self.width):
                        for j in range(0, self.height):
                            self.bStream.writeBits(v[i][j], 1)
                    self.bStream.writeAll()

    def read(self):
        f=open(self.filename, "rb")
        nFrame = 0
        #read header with info of the video
        frame=f.readline().decode('utf-8')
        #Maybe read size of the images
        rgb=np.zeros((self.width,self.height,3), dtype=np.uint8)
        if self.mode=='4:4:4':
            #for i in range(0, 2):
                    self.frame_len=self.width*self.height*3
                #while True:
                    startTime = time.time()
                    x=f.readline() # read word Frame
                    raw = f.read(self.frame_len)
                #try:
                    y = np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height)
                    u= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height)
                    v= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height*2)
                    y = y.reshape(self.width,self.height)
                    u=u.reshape(self.width,self.height)
                    v=v.reshape(self.width,self.height)
                    self.bStream.setMatrix('y')
                    self.writeData(y, '1')
                    self.bStream.setMatrix('u')
                    self.writeData(u, '1')
                    self.bStream.setMatrix('v')
                    self.writeData(v, '1')
                    nFrame+=1
                    executionTime = time.time() - startTime
                    self.totalTime += executionTime
                    self.bStream.writeAll('out.txt')
                    print("Frame {} took {} seconds".format(nFrame, round(executionTime)))
                    self.bStream.resetAll()
                    #time.sleep(10)
                #except:
                    #break
                    #pass
            #print(self.totalTime)



    def writeData(self, matrix, predictorType):
        for i in range(0, self.width):
            for j in range(0, self.height):
                x = int(matrix[i][j])
                p = int(self.predictor(matrix, i, j, predictorType))
                e = x - p
                if e < 0:
                    e = 2*abs(e) - 1
                else:
                    e = 2*e
                enc = self.gol.encode(e)
                nu = ''.join(str(e) for e in enc)
                self.bStream.writeBits(int(nu,2), len(enc))
                #print(x)
                #print(e)
                #print(enc)
                #time.sleep(1)

    def predictor(self,matrix, i, j, tipo):
        a = 0
        b = 0
        c = 0
        if tipo == '1':
            if j > 0:
                return matrix[i][j-1]
            return 0
        elif tipo == '2':
            if i > 0:
                return matrix[i-1][j]
            return 0
        elif tipo == '3':
            if i > 0 and j > 0:
                return matrix[i-1][j-1]
            return 0
        else:
            if j > 0:
                a = matrix[i][j-1]
                if i > 0:
                    b = matrix[i-1][j]
                    c = matrix[i-1][j-1]
            elif i > 0:
                b = matrix[i-1][j]
            if tipo == '4':
                return a + b -c
            elif tipo == '5':
                return a + (b-c)/2
            elif tipo == '6':
                return b + (a-c)/2
            elif tipo == '7':
                return (a+b)/2
            elif tipo == 'jpegLS':
                if c >= max(a,b):
                    return min(a,b)
                elif c <= min(a,b):
                    return max(a,b)
                else:
                    return int(a)+int(b)-int(c)
#falta meter o jpeg!!!!

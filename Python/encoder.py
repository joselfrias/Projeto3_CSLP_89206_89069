from PIL import Image
import numpy as np
from Golomb import Golomb
from BitStream import Stream
import time

#Class of the intraframe codec
#
#Uses Golomb class to encode and decode data, BitStream class to write and read from
# a file.


class Encoder:
    def __init__(self, filename,mode):
        self.filename=filename
        self.mode=mode
        self.width=1280
        self.height=720
        self.frame_len=0
        self.bStream = Stream()
        self.gol = Golomb(4)
        self.totalTime = 0

##Function that reads a compressed file, decompresses it and shows each frame
    def showEncodedImage(self):
        file = open('encodedFrames.txt', 'rb')
        if self.mode == '4:4:4':
            while True:
                try:
                    yMatrix = np.zeros((self.height, self.width ), dtype=np.uint8)
                    uMatrix = np.zeros((self.height,self.width), dtype=np.uint8)
                    vMatrix = np.zeros((self.height,self.width), dtype=np.uint8)
                    tim = time.time()
                    yMatrix = self.readData(yMatrix, '1', file, 'y')
                    uMatrix = self.readData(uMatrix, '1', file, 'u')
                    vMatrix = self.readData(vMatrix, '1', file, 'v')
                    rgb=np.zeros((self.height, self.width,3),dtype=np.uint8)
                    yMatrix=yMatrix.reshape(self.height,self.width)
                    uMatrix=uMatrix.reshape(self.height,self.width)
                    vMatrix=vMatrix.reshape(self.height,self.width)
                    for i in range(0, self.height):
                        for j in range(0, self.width):
                            rgb[i][j] = [yMatrix[i][j]+1.403*(vMatrix[i][j]-128),yMatrix[i][j]-0.714*(vMatrix[i][j]-128)-0.344*(uMatrix[i][j]-128),yMatrix[i][j]+1.773*(uMatrix[i][j]-128)]
                    img = Image.fromarray(rgb, 'RGB')
                    img.show()
                except:
                    break
        elif self.mode == '4:2:2':
            while True:
                try:
                    yMatrix = np.zeros((self.height, self.width), dtype=np.uint8)
                    uMatrix = np.zeros((self.height, self.width), dtype=np.uint8)
                    vMatrix = np.zeros((self.height, self.width), dtype=np.uint8)
                    tim = time.time()
                    file = open('encodedFrames.txt', 'rb')
                    yMatrix = self.readData(yMatrix, '1', file, 'y')
                    uMatrix = self.readData(uMatrix, '1', file, 'u')
                    vMatrix = self.readData(vMatrix, '1', file, 'v')
                    rgb=np.zeros((self.height, self.width,3),dtype=np.uint8)
                    uMatrix=np.resize(uMatrix, (self.height, self.width))
                    vMatrix=np.resize(vMatrix, (self.height, self.width))
                    yMatrix=yMatrix.reshape(self.height,self.width)
                    uMatrix=uMatrix.reshape(self.height,self.width)
                    vMatrix=vMatrix.reshape(self.height,self.width)
                    for i in range(0, self.height):
                        for j in range(0, self.width):
                            rgb[i][j] = [yMatrix[i][j]+1.403*(vMatrix[i][j]-128),yMatrix[i][j]-0.714*(vMatrix[i][j]-128)-0.344*(uMatrix[i][j]-128),yMatrix[i][j]+1.773*(uMatrix[i][j]-128)]
                    img = Image.fromarray(rgb, 'RGB')
                    img.show()
                else:
                    break
        elif self.mode == '4:2:2':
            while True:
                try:
                    yMatrix = np.zeros((self.height, self.width), dtype=np.uint8)
                    uMatrix = np.zeros((self.height, self.width), dtype=np.uint8)
                    vMatrix = np.zeros((self.height, self.width), dtype=np.uint8)
                    tim = time.time()
                    file = open('encodedFrames.txt', 'rb')
                    yMatrix = self.readData(yMatrix, '1', file, 'y')
                    uMatrix = self.readData(uMatrix, '1', file, 'u')
                    vMatrix = self.readData(vMatrix, '1', file, 'v')
                    rgb=np.zeros((self.height, self.width,3),dtype=np.uint8)
                    uMatrix=np.resize(uMatrix, (self.height, self.width))
                    vMatrix=np.resize(vMatrix, (self.height, self.width))
                    yMatrix=yMatrix.reshape(self.height,self.width)
                    uMatrix=uMatrix.reshape(self.height,self.width)
                    vMatrix=vMatrix.reshape(self.height,self.width)
                    for i in range(0, self.height):
                        for j in range(0, self.width):
                            rgb[i][j] = [yMatrix[i][j]+1.403*(vMatrix[i][j]-128),yMatrix[i][j]-0.714*(vMatrix[i][j]-128)-0.344*(uMatrix[i][j]-128),yMatrix[i][j]+1.773*(uMatrix[i][j]-128)]
                    img = Image.fromarray(rgb, 'RGB')
                    img.show()
                except:
                    break
        file.close()

##Sub-function used by showEncodedImage, uses both Golomb and BitStream to return a matrix of each component with data 
    def readData(self, matrix, predictorType, file, component):
        for i in range(0, self.height):
            for j in range(0, self.width):
                y = []
                while True:
                    nBit = self.bStream.readbits(1, file)
                    y.append(nBit)
                    if nBit == 0:
                        for c in range(0, 2):
                            y.append(self.bStream.readbits(1, file))
                        break
                dec = self.gol.decode(y)
                if dec%2 == 0:
                    e = dec/2
                else:
                    e = -1*((dec+1)/2)
                p = int(self.predictor(matrix, i, j, '1'))
                x = int(e + p)
                matrix[i][j] = x
        return matrix

##Function that reads a video file, compresses it and writes it down
    def read(self):
        f=open(self.filename, "rb")
        nFrame = 0
        #read header with info of the video
        frame=f.readline().decode('utf-8')
        self.width = int(frame.split(" ")[1][1:])
        self.height = int(frame.split(" ")[2][1:])
        #Maybe read size of the images
        rgb=np.zeros((self.width,self.height,3), dtype=np.uint8)
        if self.mode=='4:4:4':
            #for i in range(0, 2):
                self.frame_len=self.width*self.height*3
                while True:
                        startTime = time.time()
                        x=f.readline() # read word Frame
                        raw = f.read(self.frame_len)
                        try:
                            y = np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height)
                            u= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height)
                            v= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height*2)
                            y = y.reshape(self.height,self.width)
                            u=u.reshape(self.height,self.width)
                            v=v.reshape(self.height,self.width)
                            self.bStream.setMatrix('y')
                            self.writeData(y, '1', self.mode, 'y')
                            self.bStream.setMatrix('u')
                            self.writeData(u, '1', self.mode, 'u')
                            self.bStream.setMatrix('v')
                            self.writeData(v, '1', self.mode, 'v')
                            nFrame+=1
                            executionTime = time.time() - startTime
                            self.totalTime += executionTime
                            self.bStream.writeAll('encodedFrames.txt')
                            print("Frame {} took {} seconds".format(nFrame, round(executionTime)))
                            self.bStream.resetAll()
                        except:
                            break
        elif self.mode == '4:2:2':
            self.frame_len= self.width*self.height*2
            #while True:
            for ka in range(0,3):
                startTime = time.time()
                x = f.readline()
                raw = f.read(self.frame_len)
                try:
                    y = np.frombuffer(raw, dtype=np.uint8, count=self.width*self.height)
                    u = np.frombuffer(raw, dtype=np.uint8, count=int(self.width*self.height*0.5), offset=self.width*self.height)
                    v = np.frombuffer(raw, dtype=np.uint8, count=int(self.width*self.height*0.5), offset=int(self.width*self.height*1.5))
                    u=np.resize(u, (self.height, self.width))
                    v=np.resize(v, (self.height, self.width))
                    y = y.reshape(self.height,self.width)
                    u=u.reshape(self.height,self.width)
                    v=v.reshape(self.height,self.width)
                    self.bStream.setMatrix('y')
                    self.writeData(y, '1', 'y')
                    self.bStream.setMatrix('u')
                    self.writeData(u, '1', 'u')
                    self.bStream.setMatrix('v')
                    self.writeData(v, '1', 'v')
                    nFrame+=1
                    executionTime = time.time() - startTime
                    self.totalTime += executionTime
                    self.bStream.writeAll('encodedFrames.txt')
                    print("Frame {} took {} seconds".format(nFrame, round(executionTime)))
                    self.bStream.resetAll()
                except:
                    pass
        elif self.mode == '4:2:0':
            self.frame_len= self.width*self.height*1.5
            while True:
                startTime = time.time()
                x = f.readline()
                raw = f.read(self.frame_len)
                try:
                    y = np.frombuffer(raw, dtype=np.uint8, count=self.width*self.height)
                    u = np.frombuffer(raw, dtype=np.uint8, count=self.width*self.height*0.25, offset=self.width*self.height)
                    v = np.frombuffer(raw, dtype=np.uint8, count=self.width*self.height*0.25, offset=self.width*self.height*1.25)
                    u=np.resize(u, (self.height, self.width))
                    v=np.resize(v, (self.height, self.width))
                    y = y.reshape(self.height,self.width)
                    u=u.reshape(self.height,self.width)
                    v=v.reshape(self.height,self.width)
                    self.bStream.setMatrix('y')
                    self.writeData(y, '1', 'y')
                    self.bStream.setMatrix('u')
                    self.writeData(u, '1', 'u')
                    self.bStream.setMatrix('v')
                    self.writeData(v, '1', 'v')
                    nFrame+=1
                    executionTime = time.time() - startTime
                    self.totalTime += executionTime
                    self.bStream.writeAll('encodedFrames.txt')
                    print("Frame {} took {} seconds".format(nFrame, round(executionTime)))
                    self.bStream.resetAll()
                except:
                    break
        print(self.totalTime)

##Sub-function of read that uses Golomb to encode data and BitStream to write it on a file
    def writeData(self, matrix, predictorType, component):
        controler = 1
        if(component != 'y'):
            if(self.mode == '4:2:2'):
                controler = 0.5
            elif(self.mode == '4:2:0'):
                controler = 0.25
        for i in range(0, int(self.height*controler)):
            for j in range(0, int(self.width*controler)):
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

##Function used to predict the next value of the image matrix, used by writeData and readData
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


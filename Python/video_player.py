from PIL import Image
import numpy as np
from Golomb import Golomb
from BitStream import Stream

class VideoPlayer:
    def __init__(self, filename,mode):
        self.filename=filename
        self.mode=mode
        self.width=720
        self.height=1280
        self.frame_len=0
        self.bStream = Stream()
        self.gol = Golomb(4)


    def read(self):
        nFrame = 0
        f=open(self.filename, "rb")
        #read header with info of the video
        frame=f.readline().decode('utf-8')
        #Maybe read size of the images
        rgb=np.zeros((self.width,self.height,3), dtype=np.uint8)
        if self.mode=='4:4:4':
            self.frame_len=self.width*self.height*3
            while True:
                x=f.readline() # read word Frame
                raw = f.read(self.frame_len)
                try:
                    y = np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height)
                    u= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height)
                    v= np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height,offset=self.width*self.height*2)
                    y = y.reshape(self.width,self.height)
                    u=u.reshape(self.width,self.height)
                    v=v.reshape(self.width,self.height)
                    tipo = 1
                    nFrame +=1
                except:
                    break
                '''for i in range(0, self.width):
                    for j in range(0, self.height):
                    	x = int(y[i][j])
                    	p = int(self.predictor(y, i, j, tipo))
                    	e = x - p
                    	if e < 0:
                    		pass
                    	x=2e if e>0
                    	x=2|e| -1 if e<0	
                    	self.gol.encode(e)
                        #rgb[i][j]=[y[i][j]+1.403*(v[i][j]-128),y[i][j]-0.714*(v[i][j]-128)-0.344*(u[i][j]-128),y[i][j]+1.773*(u[i][j]-128)]
                #img = Image.fromarray(rgb, 'RGB')
                #img.show()
                '''
            print(nFrame)
        elif self.mode == '4:2:2':
            self.frame_len=self.width*self.height*2
            while True:
                header=f.readline()
                print (header.decode('utf-8'))
                self.frame_len=self.width*self.height*3
                raw = f.read(self.frame_len)
                y = np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height)
                u= np.frombuffer(raw, dtype=np.uint8,count=int(self.width*self.height*0.5),offset=int(self.width*self.height))
                v= np.frombuffer(raw, dtype=np.uint8,count=int(self.width*self.height*0.5),offset=int(self.width*self.height*1.5))

                u=np.resize(u, (self.width, self.height))
                v=np.resize(v, (self.width, self.height))
                y = y.reshape(self.width, self.height)
                u=u.reshape(self.width, self.height)
                v=v.reshape(self.width, self.height)
                for i in range(0, self.width):
                    for j in range(0, self.height):
                        rgb[i][j]=[y[i][j]+1.403*(v[i][j]-128),y[i][j]-0.714*(v[i][j]-128)-0.344*(u[i][j]-128),y[i][j]+1.773*(u[i][j]-128)]

                img = Image.fromarray(rgb)
                img.show()

        elif self.mode == '4:2:0':
            self.frame_len=int(self.width*self.height*(3/2))
            while True:
                header=f.readline()
                raw = f.read(self.frame_len)
                y = np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height)
                u= np.frombuffer(raw, dtype=np.uint8,count=int(self.width*self.height*0.25),offset=int(self.width*self.height))
                v= np.frombuffer(raw, dtype=np.uint8,count=int(self.width*self.height*0.25),offset=int(self.width*self.height*0.25))

                u=np.resize(u, (self.width,self.height))
                v=np.resize(v, (self.width,self.height))

                y = y.reshape(self.width,self.height)
                u=u.reshape(self.width,self.height)
                v=v.reshape(self.width,self.height)

                for i in range(0, self.width):
                    for j in range(0, self.height):
                        rgb[i][j]=[y[i][j]+1.403*(v[i][j]-128),y[i][j]-0.714*(v[i][j]-128)-0.344*(u[i][j]-128),y[i][j]+1.773*(u[i][j]-128)]

                img = Image.fromarray(rgb)
                #img.save('my.png')
                img.show()

    def predictor(self,matrix, i, j, tipo):
    	a = 0
    	b = 0
    	c = 0
    	tipo = int(tipo)
    	if tipo == 1:
    		if j > 0:
    			return matrix[i][j-1]
    		return 0
    	elif tipo == 2:
    		if i > 0:
    			return matrix[i-1][j]
    		return 0
    	elif tipo == 3:
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
    		if tipo == 4:
    			return a + b -c
    		elif tipo == 5:
    			return a + (b-c)/2
    		elif tipo == 6:
    			return b + (a-c)/2
    		elif tipo == 7:
    			return (a+b)/2
#falta meter o jpeg!!!!

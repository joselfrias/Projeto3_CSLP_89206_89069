from PIL import Image
import numpy as np
class VideoPlayer:
    def __init__(self, filename,mode):
        self.filename=filename
        self.mode=mode
        self.width=720
        self.height=1280
        self.frame_len=0


    def read(self):
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
                y = np.frombuffer(raw, dtype=np.uint8,count=self.width*self.height)
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

        elif self.mode == '4:2:2':
            self.frame_len=self.width*self.height*2
            while True:
                header=f.readline()
                print (header.decode('utf-8'))
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

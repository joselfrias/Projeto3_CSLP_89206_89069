import numpy as np
from PIL import Image
rgb=np.zeros((720,1280,3), dtype=np.uint8)
def main():
    file='ducks_take_off_420_720p50.y4m'
    f=open(file, 'rb')

    frame=f.readline().decode('utf-8')
    print (frame)
    header=f.readline()
    print (header.decode('utf-8'))
    while True:

        raw = f.read(int(1280*720*(3/2)))
        y = np.frombuffer(raw, dtype=np.uint8,count=1280*720)
        u= np.frombuffer(raw, dtype=np.uint8,count=int(1280*720*0.25),offset=int(1280*720))
        v= np.frombuffer(raw, dtype=np.uint8,count=int(1280*720*0.25),offset=int(1280*720*0.25))

        u=np.resize(u, (720, 1280))
        v=np.resize(v, (720, 1280))
        y = y.reshape(720, 1280)
        u=u.reshape(720,1280)
        v=v.reshape(720,1280)



        for i in range(0, 720):
            for j in range(0, 1280):
                rgb[i][j]=[y[i][j]+1.14*v[i][j],y[i][j]-0.395*u[i][j]-0.581*v[i][j],y[i][j]+2.032*u[i][j]]

        img = Image.fromarray(rgb)
        #img.save('my.png')
        img.show()




main()

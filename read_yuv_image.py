import numpy as np
def main():
    file='ducks_take_off_444_720p50.y4m'
    f=open(file, 'rb')
    count_frame=0

    frame=f.readline().decode('utf-8')
    print (frame)
    header=f.readline()
    print (header.decode('utf-8'))
    while True:



        raw = f.read(int(1280*720*3))
        y = np.frombuffer(raw, dtype=np.uint8,count=1280*720)
        u= np.frombuffer(raw, dtype=np.uint8,count=1280*720,offset=1280*720)
        v= np.frombuffer(raw, dtype=np.uint8,count=1280*720,offset=1280*720*2)

        y = y.reshape(720, 1280)
        u=u.reshape(720,1280)
        v=v.reshape(720,1280)
        print (len(y))

        count_frame +=1
        print (count_frame)
        #nextline=f.readline()
        #print (nextline)
    print (count_frame)






main()

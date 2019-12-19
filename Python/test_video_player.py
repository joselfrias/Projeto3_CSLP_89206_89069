#from video_player import *
from encoder import Encoder
from timeEncoder import TimeEncoder
def main():
    #vp=VideoPlayer('ducks_take_off_444_720p50.y4m','4:4:4')
    #vp.read()
    en = Encoder('ducks_take_off_444_720p50.y4m','4:4:4')
    #en.showImage()
    #en.read()
    #en.showEncodedImage()
    #en.realSpace()
    ten = TimeEncoder('ducks_take_off_444_720p50.y4m', '4:4:4')
    ten.encode()
    en.showEncodedImage()





main()


'''
 self.out = open("out.txt", "wb")
        if self.matrix == 'y':
            for coisa in self.y:
                self.out.write(bytearray([coisa]))
            self.y = []
        elif self.matrix == 'u':
            for coisa in self.u:
                self.out.write(bytearray([coisa]))
            self.u = []
        elif self.matrix == 'v':
            for coisa in self.v:
                self.out.write(bytearray([cosia]))
            self.v = []
'''
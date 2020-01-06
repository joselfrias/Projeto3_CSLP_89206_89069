from video_player import *
from encoder import Encoder
#from timeEncoder import TimeEncoder
def main():
    #vp=VideoPlayer('ducks_take_off_444_720p50.y4m','4:4:4')
    #vp = VideoPlayer('ducks_take_off_422_720p50.y4m', '4:2:2')
    #vp=VideoPlayer('ducks_take_off_420_720p50.y4m','4:2:0')
    #vp.read()
    #en = Encoder('ducks_take_off_444_720p50.y4m','4:4:4')
    en = Encoder('ducks_take_off_422_720p50.y4m','4:2:2')
    #en.showImage()
    #en.read()
    en.showEncodedImage()
    #en.realSpace()
    #ten = TimeEncoder('ducks_take_off_444_720p50.y4m', '4:4:4')
    #ten.encode()
    #en.showEncodedImage()





main()



#include "Encoder.h"

int main(){
	Encoder enc = Encoder("ducks_take_off_444_720p50.y4m");
	enc.encode();
	//enc.decode();
	//enc.compress("ducks_take_off_444_720p50.y4m");
	//enc.weirdTest();
	return 0;
}
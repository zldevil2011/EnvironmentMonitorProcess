#include<stdlib.h>

void StringToHex(char InputStr[], char OutputHex[], uint32_t InputLen)
{
	for (uint32_t i = 0;i < InputLen;)
	{
		if (InputStr[i] >= 0x30 && InputStr[i] <= 0x39)
			OutputHex[i/2] = (InputStr[i] - 0x30) << 4;
		else
			OutputHex[i/2] = (InputStr[i] - 0x37) << 4;

		if (InputStr[i + 1] >= 0x30 && InputStr[i + 1] <= 0x39)
			OutputHex[i/2] |= (InputStr[i + 1] - 0x30) ;
		else
			OutputHex[i/2] |= (InputStr[i + 1] - 0x37);
		i += 2;
	}
}
int main(){
    return 0;
}
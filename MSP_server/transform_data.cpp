#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define SensorNum   12
const char * base64char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

typedef struct sMinTime
{
  unsigned int year : 6;
  unsigned int month : 4;
  unsigned int date : 5;
  unsigned int hour : 5;
  unsigned int min : 6;
  unsigned int sec : 6;
}sMinTime;

#define SensorConfigBitTime            ((unsigned int)0x1)
#define SensorConfigBitBatteryVol      ((unsigned int)0x2)
#define SensorConfigBitSolarEnergyVol  ((unsigned int)0x4)
#define SenSorConfigBitO3Data          ((unsigned int)0x8)
#define SenSorConfigBitCOData          ((unsigned int)0x10)
#define SenSorConfigBitSO2Data         ((unsigned int)0x20)
#define SenSorConfigBitNO2Data         ((unsigned int)0x40)
#define SenSorConfigBitPM25Data        ((unsigned int)0x80)
#define SenSorConfigBitPM10Data        ((unsigned int)0x100)
#define SensorConfigBitTData           ((unsigned int)0x200)
#define SensorConfigBitPData           ((unsigned int)0x400)
#define SensorConfigBitHumData         ((unsigned int)0x800)


bool IsBigEndian() {
  union NUM {
    int a;
    char b;
  }num;
  num.a = 0x1234;
  if (num.b == 0x12) {
    return true;
  }
  return false;
}
sMinTime MinTime;
unsigned short temp[SensorNum + 7];
unsigned short config;
extern "C"{
void  AnalyzeData(char InputStr[], unsigned short OutStr[])
{
  memcpy(&MinTime, (unsigned int *)&InputStr[4], 4);
  OutStr[0] = MinTime.year;
  OutStr[1] = MinTime.month;
  OutStr[2] = MinTime.date;
  OutStr[3] = MinTime.hour;
  OutStr[4] = MinTime.min;
  OutStr[5] = MinTime.sec;
  OutStr[6] = *(unsigned short *)&InputStr[0];
  config = *(unsigned short *)&InputStr[2];
  unsigned short i = 8;
  unsigned short j = 7;
  unsigned int ConfigBit = 0x2;
  for (unsigned short i = 8;i < SensorNum*2+8;)
  {
    if ((config&ConfigBit) != 0)
    {
      OutStr[j] = *(unsigned int *)&InputStr[i];
      i += 2;
    }  
    else 
      OutStr[j] = 0;
    j++;
    ConfigBit = ConfigBit << 1;
    if (ConfigBit > SensorConfigBitHumData)
      break;
  }
}
}
/*
int main()
{
  char str[50] = {
    0x0f,0x00,0xff,0x0f,0xc7,0xbc,0x55,0x01
   ,0x58,0x02,0x00,0x00,0x0d,0x00,0x8a,0x02
   ,0x03,0x00,0x14,0x00,0x89,0x00,0xa9,0x00
   ,0x78,0x07,0xcd,0x27,0xa9,0x0b,0x00,0x00
   ,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
   ,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
   ,0xca,0x55 };
  unsigned short str2[19];
  AnalyzeData(str, str2);
  return 1;
}

int base64_decode(const char * base64, unsigned char * bindata)
{
  int i, j;
  unsigned char k;
  unsigned char temp[4];
  for (i = 0, j = 0; base64[i] != '\0'; i += 4)
  {
    memset(temp, 0xFF, sizeof(temp));
    for (k = 0; k < 64; k++)
    {
      if (base64char[k] == base64[i])
        temp[0] = k;
    }
    for (k = 0; k < 64; k++)
    {
      if (base64char[k] == base64[i + 1])
        temp[1] = k;
    }
    for (k = 0; k < 64; k++)
    {
      if (base64char[k] == base64[i + 2])
        temp[2] = k;
    }
    for (k = 0; k < 64; k++)
    {
      if (base64char[k] == base64[i + 3])
        temp[3] = k;
    }

    bindata[j++] = ((unsigned char)(((unsigned char)(temp[0] << 2)) & 0xFC)) |
      ((unsigned char)((unsigned char)(temp[1] >> 4) & 0x03));
    if (base64[i + 2] == '=')
      break;

    bindata[j++] = ((unsigned char)(((unsigned char)(temp[1] << 4)) & 0xF0)) |
      ((unsigned char)((unsigned char)(temp[2] >> 2) & 0x0F));
    if (base64[i + 3] == '=')
      break;

    bindata[j++] = ((unsigned char)(((unsigned char)(temp[2] << 6)) & 0xF0)) |
      ((unsigned char)(temp[3] & 0x3F));
  }
  return j;
}
*/
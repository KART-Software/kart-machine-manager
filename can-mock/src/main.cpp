// demo: CAN-BUS Shield, send data
// loovee@seeed.cc

#include <Arduino.h>
#include <SPI.h>

#define CAN_2515
// #define CAN_2518FD

// Set SPI CS Pin according to your hardware

#if defined(SEEED_WIO_TERMINAL) && defined(CAN_2518FD)
// For Wio Terminal w/ MCP2518FD RPi Hat：
// Channel 0 SPI_CS Pin: BCM 8
// Channel 1 SPI_CS Pin: BCM 7
// Interupt Pin: BCM25
const int SPI_CS_PIN = BCM8;
const int CAN_INT_PIN = BCM25;
#else

// For Arduino MCP2515 Hat:
// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;
#endif

#ifdef CAN_2518FD
#include "mcp2518fd_can.h"
mcp2518fd CAN(SPI_CS_PIN); // Set CS pin
#endif

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin
#endif

struct MachineLog
{
  uint16_t r, tp, et, ot, op, gv, bv, l, mp, fp;
  void update()
  {
    uint32_t t = millis();
    r = t % 9500;
    tp = t % 1000;
    et = t % 1200;
    ot = t % 1500;
    op = t % 2000;
    gv = t % 5000;
    bv = t % 12000;
    l = t % 1400;
    mp = t % 1000;
    fp = t % 3000;
  }

  void toSendData0(byte *sendData)
  {
    uint16_t data[4] = {r, tp, et, ot};
    for (int i = 0; i < 4; i++)
    {
      sendData[2 * i] = lowByte(data[i]);
      sendData[2 * i + 1] = highByte(data[i]);
    }
  }

  void toSendData1(byte *sendData)
  {
    uint16_t data[4] = {op, gv, bv, l};
    for (int i = 0; i < 4; i++)
    {
      sendData[2 * i] = lowByte(data[i]);
      sendData[2 * i + 1] = highByte(data[i]);
    }
  }

  void toSendData2(byte *sendData)
  {
    uint16_t data[2] = {mp, fp};
    for (int i = 0; i < 2; i++)
    {
      sendData[2 * i] = lowByte(data[i]);
      sendData[2 * i + 1] = highByte(data[i]);
    }
  }
};

void setup()
{
  SERIAL_PORT_MONITOR.begin(115200);
  while (!Serial)
  {
  };

  while (CAN_OK != CAN.begin(CAN_500KBPS))
  { // init can bus : baudrate = 500k
    SERIAL_PORT_MONITOR.println("CAN init fail, retry...");
    delay(100);
  }
  SERIAL_PORT_MONITOR.println("CAN init ok!");
}

MachineLog machineLog;

void loop()
{
  machineLog.update();

  byte sendData[8];
  machineLog.toSendData0(sendData);
  CAN.sendMsgBuf(0x5F0, 0, 8, sendData);
  machineLog.toSendData1(sendData);
  CAN.sendMsgBuf(0x5F1, 0, 8, sendData);
  machineLog.toSendData2(sendData);
  CAN.sendMsgBuf(0x5F2, 0, 4, sendData);
  delay(30); // send data per 100ms
  SERIAL_PORT_MONITOR.println("CAN BUS sendMsgBuf ok!");
}

// END FILE

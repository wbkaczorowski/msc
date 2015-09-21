import os
import sys
import time
import struct

#tos stuff
sys.path.append(os.path.join(os.environ["TOSROOT"], "tools/tinyos/python"))
import SensorMoteMsg
from tinyos.message import *

class DataLogger:
    def __init__(self, motestring):
        self.mif = MoteIF.MoteIF()
        self.tos_source = self.mif.addSource(motestring)
        self.mif.addListener(self, SensorMoteMsg.SensorMoteMsg)

    def receive(self, src, msg):
        if msg.get_amType() == SensorMoteMsg.AM_TYPE:
            print msg
            m = SensorMoteMsg.SensorMoteMsg(msg.dataGet())
            print time.time(), m.get_nodeId(), m.get_lightValue()
        sys.stdout.flush()

    # def send(self):
    #             smsg = SensorMoteMsg.SensorMoteMsg()
    #             smsg.set_rx_timestamp(time.time())
    #             self.mif.sendMsg(self.tos_source, 0xFFFF,
    #             smsg.get_amType(), 0, smsg)


if __name__ == "__main__":
    try:
         dl = DataLogger("sf@localhost:9002")
         while True:
             time.sleep(1)
    except KeyboardInterrupt:
        pass
import sys
import socket
from twisted.internet.error import CannotListenError
from protocol import RPiServerProtocol
from twisted.python import log
from twisted.internet import reactor
from twisted.internet import task
from autobahn.twisted.websocket import WebSocketServerFactory
from led import LEDController
from sensor_reader import SensorReader


class RPiServer(object):
    def __init__(self, port, name, frequency, b_port, device_port, baudrate):
        self.port = port
        self.name = name
        self.broadcast_frequency = frequency
        self.broadcast_port = b_port
        self.device_port = device_port
        self.baudrate = baudrate

    def run(self):
        led = LEDController()
        # sesnor_reader = SensorReader(self.device_port, self.baudrate)

        try:
            log.startLogging(sys.stdout)
            factory = WebSocketServerFactory()
            factory.protocol = RPiServerProtocol
            factory.protocol.controller = led
            broadcast_task = task.LoopingCall(self.broadcast, factory)
            broadcast_task.start(self.broadcast_frequency)
            reactor.listenTCP(self.port, factory)
            reactor.run()
        except CannotListenError:
            print "Another server already opened at port: ", self.port
        finally:
            led.stop()


    def broadcast(self, factory):
        address = ('<broadcast>', self.broadcast_port)
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        data = self.name
        if factory.getConnectionCount() < 1:
            print "Broadcasting:", data
            broadcast_socket.sendto(data, address)



import sys
import socket, time
from twisted.internet.error import CannotListenError
from communication import RPiServerProtocol
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory
from led import LEDController



class RPiServer(object):
    def __init__(self, port, name, frequency):
        self.port = port
        self.name = name
        self.broadcast_frequency = frequency

    def run(self):
        led = LEDController()
        try:
            log.startLogging(sys.stdout)
            factory = WebSocketServerFactory()
            factory.protocol = RPiServerProtocol
            factory.protocol.controller = led
            reactor.listenTCP(self.port, factory)
            reactor.run()
            # reactor.callWhenRunning(self.broadcast)
        except CannotListenError:
            print "Another server already opened at port: ", self.port
        finally:
            led.stop()


    def broadcast(self):
        address = ('<broadcast>', self.port)
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        data = self.name
        while True:
            print data
            broadcast_socket.sendto(data, address)
            time.sleep(self.broadcast_frequency)



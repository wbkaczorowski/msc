import sys
from twisted.internet.error import CannotListenError
from communication import RPiServerProtocol
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory
from led import LEDController


class RPiServer(object):
    def __init__(self, port):
        self.port = port

    def run(self):
        led = LEDController()
        try:
            log.startLogging(sys.stdout)
            factory = WebSocketServerFactory()
            factory.protocol = RPiServerProtocol
            factory.protocol.controller = led
            reactor.listenTCP(self.port, factory)
            reactor.run()
        except CannotListenError:
            print "Another server already opened at port", self.port,
        finally:
            led.stop()

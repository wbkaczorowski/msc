import sys
from communication import RPiServerProtocol
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory
from led import LEDController


# TODO jakis config na numer portu albo cos

class RPiServer(object):
    def start(self):
        led = LEDController()

        log.startLogging(sys.stdout)
        factory = WebSocketServerFactory()
        factory.protocol = RPiServerProtocol
        factory.protocol.controller = led

        reactor.listenTCP(9000, factory)
        reactor.run()



def main():
    rpi_server = RPiServer()
    rpi_server.start()


if __name__ == "__main__":
    main()
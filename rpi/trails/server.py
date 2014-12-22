from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from RPIO import PWM

servo = PWM.Servo()


class MyServerProtocol(WebSocketServerProtocol):


    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))


    def onOpen(self):
        print("WebSocket connection open.")


    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            s = payload.decode('utf8')
            print(">>> {0}".format(s))
            servo.set_servo(23, int(s[1:3], 16))
            servo.set_servo(24, int(s[3:5], 16))
            servo.set_servo(25, int(s[5:7], 16))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        servo.stop_servo(25)
        servo.stop_servo(24)
        servo.stop_servo(23)



if __name__ == '__main__':
    import sys
    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory("ws://192.168.1.107:9000", debug=False)
    factory.protocol = MyServerProtocol
    reactor.listenTCP(9000, factory)
    reactor.run()
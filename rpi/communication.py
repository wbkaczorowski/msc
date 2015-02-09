from autobahn.twisted.websocket import WebSocketServerProtocol


class RPiServerProtocol(WebSocketServerProtocol):


    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))


    def onOpen(self):
        print("WebSocket connection open.")
        print self.controller.current_RGB
        payload = self.controller.current_RGB.encode('utf8')
        self.sendMessage(payload)


    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary data received: {0} bytes - not supported".format(len(payload)))
        else:
            s = payload.decode('utf8')
            print(">>> {0}".format(s))
            self.controller.update_rgb(s)



    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))




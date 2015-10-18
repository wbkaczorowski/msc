from autobahn.twisted.websocket import WebSocketServerProtocol
import json
import controller


class RPiServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))


    def onOpen(self):
        print("WebSocket connection open.")
        # TODO odsylanie aktualnej na telefon
        # print self.controller.current_RGB
        payload = {'color' : self.controller.led.current_RGB }
        print payload
        self.sendMessage(json.dumps(payload).encode('utf8'))


    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary data received: {0} bytes - not supported".format(len(payload)))
        else:
            s = payload.decode('utf8')
            print(">>> {0}".format(s))
            self.handleMessage(s)


    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def handleMessage(self, msg):
        data = json.loads(msg)
        if data.has_key('color'):
            self.controller.update_manual(data['color'])
        elif data.has_key('light'):
            self.controller.update_pid_point(int(data['light']))

# testing purposes
if __name__ == "__main__":

    data = "{\"light\":58}"

    print "done"
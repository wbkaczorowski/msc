from autobahn.twisted.websocket import WebSocketServerProtocol
import json
import controller
import time
import threading


class RPiServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        # TODO odsylanie aktualnej na telefon
        # print self.controller.current_RGB
        # payload = {'color': self.controller.led.current_RGB}
        # print payload
        # self.sendMessage(json.dumps(payload).encode('utf8'))
        self.connected_client = True
        self._init_read_thread()


    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary data received: {0} bytes - not supported".format(len(payload)))
        else:
            s = payload.decode('utf8')
            print(">>> {0}".format(s))
            self.handleMessage(s)


    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.connected_client = False
        try:
            if self.read_thread is not None and self.read_thread.isAlive():
                self.read_thread.join(0.01)
        except Exception as e:
            print e
            pass


    def handleMessage(self, msg):
        data = json.loads(msg)
        if data.has_key('color'):
            self.controller.update_manual(data['color'])
        elif data.has_key('light'):
            self.controller.update_pid_point(int(data['light']))
        elif data.has_key('temperature'):
            self.controller.update_temp(int(data['temperature']))

    def _init_read_thread(self):
        self.read_thread = threading.Thread(target=self.start_read_thread)
        self.read_thread.start()

    def start_read_thread(self):
        print "statrting read thread"
        allowed_keys = ["4", "6", "7"]
        while self.connected_client:
            try:
                dict = self.controller.last_reads
                for key in dict:
                    if key in allowed_keys:
                        payload = {'light': {'key': key, 'value': dict[key]}}
                        print payload
                        self.sendMessage(json.dumps(payload).encode('utf-8'))
                print "Go to sleep"
                time.sleep(0.5)
            except Exception as e:
                print e
                pass

# testing purposes
if __name__ == "__main__":

    data = "{\"light\":58}"

    print "done"
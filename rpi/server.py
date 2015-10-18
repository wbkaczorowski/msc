import sys
import socket
from twisted.internet.error import CannotListenError
from protocol import RPiServerProtocol
from twisted.python import log
from twisted.internet import reactor
from twisted.internet import task
from autobahn.twisted.websocket import WebSocketServerFactory
from controller import Controller
from led import LED
from sensor_reader import SensorReader
from pid import PID
from database import Database

class RPiServer(object):
    def __init__(self, port, name, frequency, b_port, device_port, baudrate, db_file):
        self.port = port
        self.name = name
        self.broadcast_frequency = frequency
        self.broadcast_port = b_port
        self.device_port = device_port
        self.baudrate = baudrate
        self.db_file = db_file

    def run(self):
        led = LED()
        sensor_reader = SensorReader(self.device_port, self.baudrate)
        sensor_reader.start_reading()
        # database = Database(self.db_file)
        light_controller = Controller(sensor_reader, led)

        try:
            log.startLogging(sys.stdout)
            factory = WebSocketServerFactory()
            factory.protocol = RPiServerProtocol
            factory.protocol.controller = light_controller
            broadcast_task = task.LoopingCall(self.broadcast, factory)
            broadcast_task.start(self.broadcast_frequency)
            reactor.listenTCP(self.port, factory)
            reactor.run()
        except CannotListenError:
            print "Another server already opened at port: ", self.port
        finally:
            sensor_reader.close()
            light_controller.stop()
            # database.close_connection()
            led.stop()


    def broadcast(self, factory):
        address = ('<broadcast>', self.broadcast_port)
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        data = self.name
        if factory.getConnectionCount() < 1:
            print "Broadcasting:", data
            broadcast_socket.sendto(data, address)


# testing purposes
if __name__ == "__main__":
    server = RPiServer(9000, "test", 5, 9001, 'test', 12331)
    server.run()
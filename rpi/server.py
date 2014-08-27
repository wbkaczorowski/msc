#!/usr/bin/python

 
import socket
import select
import Queue
from threading import Thread
import sys
 
class ProcessThread(Thread):
    def __init__(self):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()
 
    def add(self, data):
        self.q.put(data)
 
    def stop(self):
        self.running = False
 
    def run(self):
        q = self.q
        while self.running:
            try:
                # block for 1 second only:
                value = q.get(block=True, timeout=1)
                process(value)
            except Queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()
        #
        if not q.empty():
            print "Elements left in the queue:"
            while not q.empty():
                print q.get()
 
t = ProcessThread()
t.start()
 
def process(value):
    print ">>>"
    print value
 
def main():
    s = socket.socket()
    host = "192.168.1.14"
    port = 8234
    s.bind((host, port))
 
    print ">>> Server listening on port {p}...".format(p=port)
 
    s.listen(5)                 # Now wait for client connection.
 
    while True:
        try:
            client, addr = s.accept()
            ready = select.select([client,],[], [],2)
            if ready[0]:
                data = client.recv(4096)
                t.add(data)
        except KeyboardInterrupt:
            print
            print "Stopping server."
            break
        except socket.error, msg:
            print "Socket error %s" % msg
            break
 
    cleanup()
 
def cleanup():
    t.stop()
    t.join()
 
if __name__ == "__main__":
    main()
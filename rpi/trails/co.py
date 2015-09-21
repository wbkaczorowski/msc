import time


while True:
    try:
        start_time = time.time()
        wait_time = 1.0
        measured_value = -1
        print "co"
        while wait_time > 0:
            print wait_time
            time.sleep(0.1)
            measured_value = 0.5
            wait_time = 1.0 + start_time - time.time()
        print measured_value
    except KeyboardInterrupt:
        print "Keyboard Interrupt!"
        exit()
    except:
        pass

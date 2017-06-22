from sensor_setup import sensor_main
from button_setup import button_main
import multiprocessing
import time


# A race condition may arise from this code.
# When accessing and writing to the queue.
if __name__ == '__main__':
    try:
        q      = multiprocessing.Queue()
        sensor = multiprocessing.Process(name='sensor', \
                                         target=sensor_main, args=(q,))
        button = multiprocessing.Process(name='button', \
                                         target=button_main, args=(q,))
        sensor.start()
        time.sleep(4)
        button.start()

        sensor.join()
        button.join()

    except KeyboardInterrupt():
        sensor.join()
        button.join()

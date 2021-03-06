from sensor_setup import sensor_main
from button_setup import button_main
import multiprocessing
import time

if __name__ == '__main__':
    try:
        sensor = multiprocessing.Process(name='sensor', \
                                         target=sensor_main)
        button = multiprocessing.Process(name='button', \
                                         target=button_main)

        sensor.start()
        time.sleep(2)
        button.start()

        sensor.join()
        button.join()
    except KeyboardInterrupt():
        pass

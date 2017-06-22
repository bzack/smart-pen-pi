from sensor_setup import sensor_main
from button_setup import button_main
import threading
import time

class sensor_thread(threading.Thread):
    def run(self):
        sensor_main()
        print("{} finished!".format(self.getName()))


class button_thread(threading.Thread):
    def run(self):
        button_main()
        print("{} finished!".format(self.getName()))

if __name__ == '__main__':
    try:
        sensor = sensor_thread(name="{} Thread".format("Sensor"))
        button = button_thread(name="{} Thread".format("Button"))

        sensor.start()
        time.sleep(2)
        button.start()

        sensor.join()
        button.join()

    except KeyboardInterrupt:
        pass

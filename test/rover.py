import threading
import time
from mavHandler.roverHandler import *


class MyRoverHandler(RoverHandler):
    def __init__(self):
        super().__init__()

        self.user_thread = threading.Timer(0, self.user)
        self.user_thread.daemon = True
        self.user_thread.start()

    def user(self):
        while True:
            time.sleep(1)
            print("arm:", self.armed, "mode:", self.mode)
            print("set param:", self.set_param("CRUISE_SPEED", 2, 0))
            if self.connected:
                print("get param:", self.get_param("CRUISE_SPEED"))
                self.change_mode(MODE_GUIDED)
                self.arm(True)
                self.move(50.15189, 10.484885, 0)



if __name__ == "__main__":
    v = MyRoverHandler()
    v.enable_topics_for_read()
    v.connect("node1", rate=10)


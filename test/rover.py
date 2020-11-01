import threading
import time
from mavHandler.roverHandler import RoverHandler


class MyRoverHandler(RoverHandler):
    def __init__(self):
        super().__init__()

        self.user_thread = threading.Timer(0, self.user)
        self.user_thread.daemon = True
        self.user_thread.start()

    def user(self):
        while True:
            time.sleep(1)
            print("arm:", self.arm, "mode:", self.mode)



if __name__ == "__main__":
    v = MyRoverHandler()
    v.enable_topics_for_read()
    v.connect("node1", rate=10)


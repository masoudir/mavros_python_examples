import threading
import time

import mavros_msgs.msg
import mavros_msgs.srv

from mavHandler.rospyHandler import RosHandler
from mavHandler.topicService import TopicService


class RoverHandler(RosHandler):
    def __init__(self):
        super().__init__()
        self.arm = False
        self.mode = ""

        self.TOPIC_STATE = TopicService("/mavros/state", mavros_msgs.msg.State)
        self.SERVICE_ARM = TopicService("/mavros/cmd/arming", mavros_msgs.srv.CommandBool)

        self.thread_param_updater = threading.Timer(0, self.update_parameters_from_topic)
        self.thread_param_updater.daemon = True
        self.thread_param_updater.start()

    def enable_topics_for_read(self):
        self.topic_reader(self.TOPIC_STATE)

    def update_parameters_from_topic(self):
        while True:
            if self.connected:
                data = self.TOPIC_STATE.get_data()
                self.arm = data.armed
                self.mode = data.mode



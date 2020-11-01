import mavros_msgs.msg
import mavros_msgs.srv

from rosHandler.rosHandler import RosHandler
from rosHandler.topicService import TopicService


class RoverHandler(RosHandler):
    def __init__(self):
        super().__init__()
        self.TOPIC_STATE = TopicService("/mavros/state", mavros_msgs.msg.State)
        self.SERVICE_ARM = TopicService("/mavros/cmd/arming", mavros_msgs.srv.CommandBool)

    def enable_topics_for_read(self):
        self.topic_reader(self.TOPIC_STATE)

v = RoverHandler()
v.enable_topics_for_read()
v.connect("node1", rate=10)




while True:
    pass



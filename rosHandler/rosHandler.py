import rospy
from rosHandler.topicService import TopicService


class RosHandler:
    def __init__(self):
        self.rate = 1
        self.connected = False

    def connect(self, node: str, rate: int):
        rospy.init_node(node, anonymous=True)
        self.rate = rospy.Rate(rate)
        rospy.spin()
        self.connected = True

    def disconnect(self):
        if self.connected:
            rospy.signal_shutdown("disconnect")
            self.connected = False

    @staticmethod
    def topic_reader(topic: TopicService):
        rospy.Subscriber(topic.getName(), topic.getType(), topic.setData)

    @staticmethod
    def service_caller(service: TopicService, timeout=30):
        try:
            srv = service.getName()
            typ = service.getType()
            data = service.getData()

            rospy.loginfo("waiting for ROS service:" + srv)
            rospy.wait_for_service(srv, timeout=timeout)
            rospy.loginfo("ROS service is up:" + srv)
            call_srv = rospy.ServiceProxy(srv, typ)
            return call_srv(data)
        except rospy.ROSException as e:
            print("ROS ERROR:", e)
        except rospy.ROSInternalException as e:
            print("ROS ERROR:", e)
        except KeyError as e:
            print("ERROR:", e)
        return None


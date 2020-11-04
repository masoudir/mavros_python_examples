import threading

import mavros_msgs.msg
import mavros_msgs.srv
import rospy


from mavHandler.rospyHandler import RosHandler
from mavHandler.topicService import TopicService

MODE_MANUAL = "MANUAL"
MODE_ACRO = "ACRO"
MODE_LEARNING = "LEARNING"
MODE_STEERING = "STEERING"
MODE_HOLD = "HOLD"
MODE_LOITER = "LOITER"
MODE_FOLLOW = "FOLLOW"
MODE_SIMPLE = "SIMPLE"
MODE_AUTO = "AUTO"
MODE_RTL = "RTL"
MODE_SMART_RTL = "SMART_RTL"
MODE_GUIDED = "GUIDED"
MODE_INITIALISING = "INITIALISING"

class RoverHandler(RosHandler):
    def __init__(self):
        super().__init__()
        self.armed = False
        self.mode = ""

        self.TOPIC_STATE = TopicService("/mavros/state", mavros_msgs.msg.State)
        self.SERVICE_ARM = TopicService("/mavros/cmd/arming", mavros_msgs.srv.CommandBool)
        self.SERVICE_SET_MODE = TopicService("/mavros/set_mode", mavros_msgs.srv.SetMode)
        self.SERVICE_SET_PARAM = TopicService("/mavros/param/set", mavros_msgs.srv.ParamSet)
        self.SERVICE_GET_PARAM = TopicService("/mavros/param/get", mavros_msgs.srv.ParamGet)
        self.TOPIC_SET_POSE_GLOBAL = TopicService('/mavros/setpoint_raw/global', mavros_msgs.msg.GlobalPositionTarget)

        self.thread_param_updater = threading.Timer(0, self.update_parameters_from_topic)
        self.thread_param_updater.daemon = True
        self.thread_param_updater.start()

    def enable_topics_for_read(self):
        self.topic_subscriber(self.TOPIC_STATE)

    def arm(self, status: bool):
        data = mavros_msgs.srv.CommandBoolRequest()
        data.value = status
        self.SERVICE_ARM.set_data(data)
        result = self.service_caller(self.SERVICE_ARM, timeout=30)
        return result.success, result.result

    def change_mode(self, mode: str):
        data = mavros_msgs.srv.SetModeRequest()
        data.custom_mode = mode
        self.SERVICE_SET_MODE.set_data(data)
        result = self.service_caller(self.SERVICE_SET_MODE, timeout=30)
        return result.mode_sent

    def move(self, lat: float, lon: float, alt: float):
        data = mavros_msgs.msg.GlobalPositionTarget()
        data.latitude = lat
        data.longitude = lon
        data.altitude = alt
        self.TOPIC_SET_POSE_GLOBAL.set_data(data)
        self.topic_publisher(topic=self.TOPIC_SET_POSE_GLOBAL)

    def get_param(self, param: str):
        data = mavros_msgs.srv.ParamGetRequest()
        data.param_id = param
        self.SERVICE_GET_PARAM.set_data(data)
        result = self.service_caller(self.SERVICE_GET_PARAM, timeout=30)
        return result.success, result.value.integer, result.value.real

    def set_param(self, param: str, value_integer: int, value_real: float):
        data = mavros_msgs.srv.ParamSetRequest()
        data.param_id = param
        data.value.integer = value_integer
        data.value.real = value_real
        self.SERVICE_SET_PARAM.set_data(data)
        result = self.service_caller(self.SERVICE_SET_PARAM, timeout=30)
        return result.success, result.value.integer, result.value.real

    def update_parameters_from_topic(self):
        while True:
            if self.connected:
                data = self.TOPIC_STATE.get_data()
                self.armed = data.armed
                self.mode = data.mode

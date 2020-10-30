import rospy
from mavros_msgs.srv import CommandBool
import mavros_msgs.msg

arm_status = False


def callback(data):
    print("Robot Arm Status:", data.armed)
    global arm_status
    arm_status = data.armed


def listener_caller():
    rospy.init_node('listener_caller', anonymous=True)
    rospy.Subscriber("/mavros/state", mavros_msgs.msg.State, callback)
    rate = rospy.Rate(10)
    rospy.loginfo("waiting for ROS services")
    service_timeout = 30
    try:
        rospy.wait_for_service('/mavros/cmd/arming', service_timeout)
        rospy.loginfo("ROS service is Up")
    except rospy.ROSException:
        print("Failed")

    set_arming_srv = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
    global arm_status
    while not rospy.is_shutdown():
        if not arm_status:
            set_arming_srv(True)
        rate.sleep()
    rospy.spin()


if __name__ == "__main__":
    try:
        listener_caller()
    except rospy.ROSInternalException:
        pass



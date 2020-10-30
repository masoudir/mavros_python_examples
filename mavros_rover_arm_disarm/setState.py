import rospy
from mavros_msgs.srv import CommandBool


def caller():
    rospy.init_node('caller', anonymous=True)
    rate = rospy.Rate(10)
    rospy.loginfo("waiting for ROS services")
    service_timeout = 30
    try:
        rospy.wait_for_service('/mavros/cmd/arming', service_timeout)
        rospy.loginfo("ROS service is Up")
    except rospy.ROSException:
        print("Failed")

    set_arming_srv = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
    set_arming_srv(True)
    rospy.spin()

if __name__ == "__main__":
    try:
        caller()
    except rospy.ROSInternalException:
        pass



import rospy
import mavros_msgs.msg


def callback(data):
    print("all data is:", data)
    print("Robot Arm Status:", data.armed)


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/mavros/state", mavros_msgs.msg.State, callback)
    rospy.spin()


if __name__ == "__main__":
    listener()


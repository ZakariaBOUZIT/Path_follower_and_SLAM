#!/usr/bin/env python3

import rospy
import geometry_msgs.msg
from geometry_msgs.msg import Twist, Pose, Point, PoseStamped, Quaternion, Vector3
from nav_msgs.msg import Path
import tf
import tf2_ros
from calculations import FigureEight


class Trajectory():
    """ Publish a geometry_msgs/Twist of the calculated linear and angular
    velocity to the tertlebot's cmd_vel at a fixed rate 
    """
    def __init__(self):
        self.W = 5    # width of the figure eight
        self.H = 4 # height of the figure eight
        self.T = 60  # amount of time it takes to complete the figure eight
        self.R = 1000 # frequency at which to publish the messages
        
        self.pub_turtle1_vel = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size = 10) 
        self.pub_vel = rospy.Publisher("/cmd_vel", Twist, queue_size = 10)
        self.path_pub = rospy.Publisher("path", Path, queue_size = 10)
        
        self.figure_eight = FigureEight(self.T, self.H, self.W)
        self.rate = rospy.Rate(self.R)
        self._t = 0
        self.delta_t_paused = 0
        self.init_t = rospy.get_time()
        self.round = 1
        self.path = Path()
        self.path.poses = []
        self.x = None
        self.y = None

        
        self.br = tf2_ros.StaticTransformBroadcaster() # static transform between world to odom frame

        static_transformStamped = geometry_msgs.msg.TransformStamped()
        static_transformStamped.header.stamp = rospy.Time.now()
        static_transformStamped.header.frame_id = "world"
        static_transformStamped.child_frame_id = "odom"

        static_transformStamped.transform.translation.x = 0
        static_transformStamped.transform.translation.y = 0
        static_transformStamped.transform.translation.z = 0
        quat = tf.transformations.quaternion_from_euler(0, 0, 1.08) # the angle of the turtle at (0,0,0) - from calculation
        static_transformStamped.transform.rotation.x = quat[0]
        static_transformStamped.transform.rotation.y = quat[1]
        static_transformStamped.transform.rotation.z = quat[2]
        static_transformStamped.transform.rotation.w = quat[3]
        self.br.sendTransform(static_transformStamped)
        


    def turtlebot_twist(self):
        self.x, self.y, v, omega = self.figure_eight.get_velocity(self._t)
        return Twist(linear = Vector3(x = v, y = 0, z = 0),
                    angular = Vector3(x = 0, y = 0, z = omega))


    def move(self):
        self.path.header.stamp = rospy.Time.now()
        self.path.header.frame_id = "world"
        self.path.poses.append(PoseStamped(header = self.path.header, 
                                        pose = Pose(
                                            position = Point(self.x, self.y, 0), 
                                            orientation = Quaternion(0, 0, 0, 1))))
        self.path_pub.publish(self.path)
        self._t = rospy.get_time() - self.init_t - self.delta_t_paused
        
        twist = self.turtlebot_twist()
        
        self.pub_turtle1_vel.publish(twist)
        self.pub_vel.publish(twist)
        if int(self._t/self.round) == self.T:
            self.path.poses = []
            self.round += 1


    def run(self):
        while not rospy.is_shutdown():
            self.move()


def main():
    rospy.init_node('trajectory')
    traj = Trajectory()
    traj.run()
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
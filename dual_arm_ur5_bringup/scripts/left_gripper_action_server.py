#!/usr/bin/env python



import rospy, actionlib
import thread

from control_msgs.msg import GripperCommandAction
from std_msgs.msg import Float64
from math import asin

class ParallelGripperActionController:
   
    def __init__(self):
        rospy.init_node('left_gripper_controller')
        #rospy.logwarn("parallel_gripper_action_controller.py is deprecated and will be removed in ROS Indigo, please use gripper_controller")

        # trapezoid model: base width connecting each gripper's rotation point
            #              + length of gripper fingers to computation point
            #              = compute angles based on a desired width at comp. point
        
        # publishers
       
        self.l_pub = rospy.Publisher('l_gripper_controller/command', Float64, queue_size=10)

        # subscribe to command and then spin
        self.server = actionlib.SimpleActionServer('~gripper_action', GripperCommandAction, execute_cb=self.actionCb, auto_start=False)
        self.server.start()
        rospy.spin()

    def actionCb(self, goal):
        """ Take an input command of width to open gripper. """
        rospy.loginfo('Gripper controller action goal recieved:%f' % goal.command.position)
        command = goal.command.position
        
        # publish msgs
        
        lmsg = Float64(command)
        
        self.l_pub.publish(lmsg)
        rospy.sleep(5.0)
        self.server.set_succeeded()
        rospy.loginfo('Gripper Controller: Done.')

if __name__=='__main__': 
    try:
        ParallelGripperActionController()
    except rospy.ROSInterruptException:
        rospy.loginfo('Hasta la Vista...')
        


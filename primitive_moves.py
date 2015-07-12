"""Some primitive movement definitions"""
from time import sleep
from Queue import Queue

def go_straight(distance):
    """
    Travel forwards or backwards in a straight line.
    :param distance: Distance to travel, in millimetres. +ve for forwards, -ve for backwards
    :return: 0 for success; 1 for failure
    """
    print "straight:\t{0}mm".format(distance)

def rotate(degrees):
    """
    Rotate the bot while stationary.
    :param degrees: Number of degrees to rotate, +ve for clockwise, -ve for anticlockwise
    :return: 0 for success; 1 for failure
    """
    print "rotate:\t{0} deg".format(degrees)

def rotate_min(heading):
    """
    Slightly smarter stationary rotate method which chooses its own direction of rotation
    :param heading: New heading to point towards (0-360)
    :return: 0 for success; 1 for failure
    """
    heading = heading % 360
    if 180 - heading >= 0:
        rotate(heading)
    else:
        rotate(-(360 - heading))

class CommStack(Queue):

    @classmethod
    def with_commands(cls, comms):
        comstack = cls()
        for com in comms:
            comstack.put(com)
        return comstack

    def exec_stack(self, wait_time=0):
        """
        Execute each command in the stack in sequence
        :param control_stack: the sequence of commands to run
        :param wait_time: number of seconds to sleep between actions
        :return: 0 for success, 1 for failure
        """
        while not self.empty():
            com = self.get()
            try:
                return_value = com()
            except AttributeError:
                print "No action for {0}".format(com)
            sleep(wait_time)
        return 0

if __name__ == "__main__":
    """ Do a quick test if this file is executed """

    control_sequence = [
        lambda: go_straight(10),
        lambda: go_straight(-10),
        lambda: rotate(90),
        lambda: rotate(-90),
        lambda: rotate_min(180),
        lambda: rotate_min(180),
        lambda: rotate_min(315),
        lambda: rotate_min(45),
        lambda: rotate_min(60),
        lambda: rotate_min(300)
        ]

    cs = CommStack.with_coms(control_sequence)
    cs.exec_stack(1)

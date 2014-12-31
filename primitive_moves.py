"""Some primitive movement definitions"""
from time import sleep

def go_straight(distance):
    """
    Travel forwards or backwards in a straight line.
    :param distance: Distance to travel, in millimetres. +ve for forwards, -ve for backwards
    :return: 0 for success; 1 for failure
    """
    pass

def rotate(degrees):
    """
    Rotate the bot while stationary.
    :param degrees: Number of degrees to rotate, +ve for clockwise, -ve for anticlockwise
    :return: 0 for success; 1 for failure
    """
    print degrees

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

def exec_stack(control_stack, wait_time=0):
    """
    Execute each command in the stack in sequence
    :param control_stack: the sequence of commands to run
    :param wait_time: number of seconds to sleep between actions
    :return: 0 for success, 1 for failure
    """
    for com in control_stack:
        print com()
        sleep(wait_time)
    return 0

if __name__ == 'main':
    """ Do a quick test if this is executed """
    control_stack = [
        go_straight(10),
        go_straight(-10),
        rotate(90),
        rotate(-90),
        rotate_min(180),
        rotate_min(180),
        rotate_min(315),
        rotate_min(45),
        rotate_min(60),
        rotate_min(300)
        ]

    exec_stack(control_stack, 1)

"""Some primitive movement definitions"""
import Robot


def go_straight(speed=50, distance=0):
    """
    Travel forwards or backwards in a straight line.
    :param speed: Speed to travel, as % of maximum
    :param distance: Distance to travel, in millimetres. +ve for forwards, -ve for backwards
    :return: 0 for success; 1 for failure
    """
    r = Robot.get_robot()
    print "straight:\t{0}mm at {1}% speed".format(distance, speed)

def rotate(speed=50, degrees=0):
    """
    Rotate the bot while stationary.
    :param degrees: Number of degrees to rotate, +ve for clockwise, -ve for anticlockwise
    :return: 0 for success; 1 for failure
    """
    r = Robot.get_robot()
    print "rotate:\t{0} deg at {1}% speed".format(degrees, speed)

def rotate_min(speed=50, heading=0):
    """
    Slightly smarter stationary rotate method which chooses its own direction of rotation
    :param heading: New heading to point towards (0-360)
    :return: 0 for success; 1 for failure
    """
    r = Robot.get_robot()
    heading = heading % 360
    if 180 - heading >= 0:
        rotate(speed, heading)
    else:
        rotate(speed, -(360 - heading))


def stop():
    """
    Stop the robot
    :return: 0 for success; 1 for failure
    """
    r = Robot.get_robot()
    r.stop()

##################################
# Helper functions for movement  #
##################################

def speed_to_power(speed_percentage):
    """Get the motor power setting for a given speed"""
    return Robot.MAX_POWER * (speed_percentage / 100.0)


if __name__ == "__main__":
    """ Do a quick test if this file is executed """

    control_sequence = [
        lambda: go_straight(distance=10),
        lambda: go_straight(distance=-10),
        lambda: rotate(degrees=90),
        lambda: rotate(degrees=-90),
        lambda: rotate_min(heading=180),
        lambda: rotate_min(heading=180),
        lambda: rotate_min(heading=315),
        lambda: rotate_min(heading=45),
        lambda: rotate_min(heading=60),
        lambda: rotate_min(heading=300)
        ]

    r = Robot.get_robot(init_commands=control_sequence)
    r.cs.exec_stack(wait_time=1)

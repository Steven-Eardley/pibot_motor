from Queue import Queue
from time import sleep

ON_PI = True
try:
    from picoborgrev.PicoBorgRev import PicoBorgRev
except ImportError:
    ON_PI = False

# The right motor power offset, as calculated by calibrate_tracks.py
R_OFFSET = 0

# The top motor power setting we'll allow the pibot to reach
MAX_POWER = 0.75

# The robot, if we've already initialised one
robot = None

def get_robot(*args, **kwargs):
    if robot:
        return robot
    elif ON_PI:
        return Robot(*args, **kwargs)
    else:
        return Sim_Robot(*args, **kwargs)

class Robot:
    def __init__(self, init_commands=None):
        self.ctl = PicoBorgRev()
        self.ctl.Init()
        self.cs = CommStack(init_commands)

        # Set the robot instance
        global robot
        robot = self

    def exec_cs(self):
        self.cs.exec_stack(wait_time=1)

    def stop(self):
        self.ctl.SetMotors(0)


class Sim_Robot:
    def __init__(self, init_commands=None):
        self.ctl = None
        self.cs = CommStack(init_commands)

        # Set the robot instance
        global robot
        robot = self

        print "Simulated Robot (sim_robot) initialised"

    def stop(self):
        print 'sim_robot stopped'


###############################################
# Class to handle command queuing for a robot #
###############################################
class CommStack(Queue):

    def __init__(self, init_commands=None):
        Queue.__init__(self)
        if init_commands:
            for com in init_commands:
                self.put(com)

    def exec_stack(self, wait_time=0):
        """
        Execute each command in the stack in sequence
        :param control_stack: the sequence of commands to run
        :param wait_time: number of seconds to sleep between actions
        :return: 0 for success, 1 for failure
        """
        res = []
        while not self.empty():
            com = self.get()
            try:
                return_value = com()
                res.append(return_value)
            except AttributeError:
                pass                            # Ignore commands we can't run
            sleep(wait_time)

        # Return failure if any command has failed.
        return int(reduce(lambda x, y: x and y, res))

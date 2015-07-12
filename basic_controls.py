from picoborgrev.PicoBorgRev import PicoBorgRev
from calibrate_tracks import get_char
import sys

class basic_controls():
    def __init__(self):
        self.ctl = PicoBorgRev()
        self.ctl.Init()

    def go(self, power=0.25):
        self.ctl.SetMotors(power)

    def stop(self):
        self.ctl.SetMotors(0)

    def right(self, power=0.5):
        self.ctl.SetMotor1(power)

    def left(self, power=0.5):
        self.ctl.SetMotor2(power)

    def back(self, power=-0.25):
        self.ctl.SetMotors(power)

if __name__ == '__main__':

    print "Simple movement controller. Press w/s to increase/decrease left track speed, o/k for the right.\
        Press <space> to stop the robot, or q to end the program to stop the robot"

    raw_input("\nPress enter key to continue, or ctrl-c to quit now.")

    pico = PicoBorgRev()
    pico.Init()
    R_SPEED = 0
    L_SPEED = 0
    SPEED_INCREMENT = 0.1
    offset = -0.05
    while True:
        try:
            pico.SetMotor1(R_SPEED + offset)
            pico.SetMotor2(L_SPEED)

            key = get_char()
            if key == 'w' or key == 'W':
                L_SPEED += SPEED_INCREMENT
            elif key == 's' or key == 'S':
                L_SPEED -= SPEED_INCREMENT
            if key == 'o' or key == 'O':
                R_SPEED += SPEED_INCREMENT
            elif key == 'k' or key == 'K':
                R_SPEED -= SPEED_INCREMENT
            elif key == ' ':
                L_SPEED = 0
                R_SPEED = 0
            elif key == 'q':
                raise KeyboardInterrupt

            print "Left: {:+.2f}\tRight: {:+.2f}".format(L_SPEED, R_SPEED)
        except KeyboardInterrupt:
            pico.SetMotors(0)
            print "Done."
            sys.exit(0)

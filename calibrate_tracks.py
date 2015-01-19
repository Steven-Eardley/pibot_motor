from picoborgrev.PicoBorgRev import PicoBorgRev
import sys, tty, termios

BASE_SPEED = 0.5
OFFSET_INCREMENT = 0.01

def get_char():
    """
    Get a single character from the terminal, un-buffered.
    :return: a single character
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

print "Calibrate the track speeds. The result will be a +/- offset for Motor1, the right track." \
      "\nThe robot will start to move forwards, with equal motor speeds. Use the +/- keys until the" \
      "robot drives in a straight line. Press q to end the program to stop the robot and print the offset."

raw_input("\nPress enter key to continue, or ctrl-c to quit without testing the offset.")

pico = PicoBorgRev()
pico.Init()
pico.SetMotors(BASE_SPEED)

offset = float(0)
while True:
    try:
        pico.SetMotor1(BASE_SPEED + offset)
        direction = get_char()
        if direction == '+' or direction == '=':
            offset += OFFSET_INCREMENT
        elif direction == '_' or direction == '-':
            offset -= OFFSET_INCREMENT
	elif direction == 'q':
	    raise KeyboardInterrupt
	
	print "{:+.2f}".format(offset)

    except KeyboardInterrupt:
        pico.SetMotors(0)
        print "Done. The final offset is {:+.2f}".format(offset)
        sys.exit(0)

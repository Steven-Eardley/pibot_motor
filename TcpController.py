"""
Control the robot via a socket.
"""
import zmq
import dill
import primitive_moves
from decorators import expect_kb_interrupt

# Used in tests
from random import randint
from time import sleep

LISTEN_HOST = "localhost"
LISTEN_PORT = 22201
SUBSCRIBE_STR = u""             # This means we will subscrible to all messages over this port.


class TcpListener:
    def __init__(self, listen_host=LISTEN_HOST, listen_port=LISTEN_PORT, subscribe_str=SUBSCRIBE_STR):
        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(zmq.SUB)
        self.socket.connect("tcp://{0}:{1}".format(listen_host, listen_port))
        self.socket.setsockopt_string(zmq.SUBSCRIBE, subscribe_str)

        self.comm_stack = primitive_moves.CommStack()

        self.listen()

    @expect_kb_interrupt
    def listen(self):
        """ Await and execute commands over TCP """
        while True:
            received = self.socket.recv_pyobj()
            funcs = dill.loads(received)
            for f in funcs:
                self.comm_stack.put(f)

            print "TcpListener: received {0} commands. Executing...".format(len(funcs))
            self.comm_stack.exec_stack(wait_time=1)


class TcpSender:
    def __init__(self, publish_port=LISTEN_PORT):
        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(zmq.PUB)
        self.socket.bind("tcp://*:{0}".format(publish_port))

        # Send nothing for the first message to wake up the connection; this usually isn't received
        self.socket.send_pyobj(None)
        sleep(0.5)

        # List of commands to send next
        self.commands = []

    @expect_kb_interrupt
    def send(self, comms=None):
        """ Send commands given, or those currently in the send list """
        if not comms or type(comms) is not list:
            comms = self.commands
            self.clear_commands()

        self.socket.send_pyobj(dill.dumps(comms))

        print "TcpSender: sent {0} commands".format(len(comms))

    def add_command(self, com):
        self.commands.append(com)

    def clear_commands(self):
        self.commands = []


##########################################################
# Demonstrator functions for the TCPController's actions #
##########################################################

@expect_kb_interrupt
def listen_test():
    print "Listening. Run publish_test() in a different thread to test."
    ctx = zmq.Context()
    sck = ctx.socket(zmq.SUB)
    sck.connect("tcp://{0}:{1}".format(LISTEN_HOST, LISTEN_PORT))
    sck.setsockopt_string(zmq.SUBSCRIBE, SUBSCRIBE_STR)

    cs = primitive_moves.CommStack()

    while True:
        received = sck.recv_pyobj()
        funcs = dill.loads(received)
        for f in funcs:
            cs.put(f)

        print "received {0} commands. Executing...".format(len(funcs))
        cs.exec_stack(wait_time=1)

@expect_kb_interrupt
def publish_test():
    ctx = zmq.Context()
    sck = ctx.socket(zmq.PUB)
    sck.bind("tcp://*:{0}".format(LISTEN_PORT))

    # Send nothing for the first message, this usually isn't received
    sck.send_pyobj(None)
    sleep(1)

    # Send a random number of commands
    for i in range(0, 10):
        commands = []
        for j in range(1, randint(1, 8)):
            commands.append(lambda: primitive_moves.go_straight(randint(1, 20)))

        sck.send_pyobj(dill.dumps(commands))
        print "iteration {0}: send {1} commands".format(i, len(commands))
        sleep(randint(1, 5))
    print "finished"

if __name__ == '__main__':
    listen_test()

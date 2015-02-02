"""
Control the robot via a socket.
"""
import zmq
import dill
import primitive_moves

# Used in tests
from random import randint
from time import sleep

LISTEN_HOST = "localhost"
LISTEN_PORT = 22201
SUBCRIBE_STR = u"" #u"pibot_motor"

class TcpController:

    def __init__(self, listen_host=LISTEN_HOST, listen_port=LISTEN_PORT, subscribe_str=SUBCRIBE_STR):
        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(zmq.SUB)
        self.socket.connect("tcp://{0}:{1}".format(listen_host, listen_port))
        self.socket.setsockopt_string(zmq.SUBSCRIBE, subscribe_str)

        self.comm_stack = primitive_moves.CommStack()

        self.listen()

    def listen(self):
        for i in range(0, 10):
            comlist = self.socket.recv_json()
            print comlist
            for com in comlist:
                self.comm_stack.put(com)
            print self.comm_stack.qsize()

        self.comm_stack.exec_stack()

def listen_test():
    print "Listening. Run publish_test() in a different thread to test."
    ctx = zmq.Context()
    sck = ctx.socket(zmq.SUB)
    sck.connect("tcp://{0}:{1}".format(LISTEN_HOST, LISTEN_PORT))
    sck.setsockopt_string(zmq.SUBSCRIBE, SUBCRIBE_STR)

    cs = primitive_moves.CommStack()

    while True:
        received = sck.recv_pyobj()
        funcs = dill.loads(received)
        for f in funcs:
            cs.put(f)

        print "received {0} commands. Executing...".format(len(funcs))
        cs.exec_stack(wait_time=1)

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

from master.handler.main_server import MainHttpServer
from master.boostrap import initialize
from master.mail import AuthHolder
from master.consts import DEFAULT_PORT
import sys


def main():
    """
    Beta version of a Simple HTTP server
       by 'Hung Huynh'
    """
    binding_port = DEFAULT_PORT
    if len(sys.argv) == 3:
        binding_port = int(sys.argv[1])
        # initialize auth holder
        AuthHolder(sys.argv[2], binding_port)
    else:
        print('Port is not provided, defaulting to ' + str(DEFAULT_PORT))

    initialize()
    MainHttpServer.start(binding_port)
    print("Termination is in progress. Please wait...")


if __name__ == "__main__":
    main()








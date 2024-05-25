from ClientSide.Client import Client
from ServerSide.Server import Server
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        Client().start()
    else:
        if sys.argv[1] == '-s':
            Server(5555).start()

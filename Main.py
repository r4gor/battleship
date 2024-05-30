from ClientSide.Client import Client
from ServerSide.Server import Server
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        Client().start()
    else:
        if sys.argv[1] == '-s':
            Server(5555).start()
        elif len(sys.argv) > 2 and sys.argv[1] == '-s':
            port = int(sys.argv[2])
            if 1500 < port < 65536:
                Server(port).start()
            else:
                print('Port must be between 1500 and 65536')

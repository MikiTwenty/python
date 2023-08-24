from videostreaming.hosting import Server
from videostreaming.utils import Clock, clear_output

# clear terminal output
clear_output()

# initialize the fps clock
clock = Clock()

# initialize the server socket
server = Server(verbose='high')

# start the server
server.connect(blocking = True)

# create a loop
while server.connected():

    # recevie a frame from the client
    receiving, frame = server.receive()

    # check if a client is connected
    if receiving:

        # recevie a frame
        receiving, frame = server.receive(show_video=True)

        # send a frame
        server.send()

# close the server socket
server.close()
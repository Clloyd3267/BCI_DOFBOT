# Sourced from https://www.geeksforgeeks.org/python-program-that-sends-and-recieves-message-from-client/

import socket

# take the server name and port name
host = '127.0.0.1'
port = 5000

# create a socket at server side
# using TCP / IP protocol
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

# bind the socket with server
# and port number
s.bind(('', port))

# allow maximum 1 connection to
# the socket
s.listen(1)

# wait till a client accept
# connection
c, addr = s.accept()

# display client address
print("CONNECTION FROM:", str(addr))

# send message to the client after
# encoding into binary string
c.send(b"HELLO, How are you ? \
       Welcome to Akash hacking World")

msg = "Bye.............."
c.send(msg.encode())

# disconnect the server
c.close()
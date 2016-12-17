"""
A example of a simple file server using Python's http and socketserver modules.
"""

import http.server
import socketserver

#
#  Pick a port to use.
#
PORT = 8000

#
#  Get the handler we want to use. This is the
#  function that will recieve and reply to the HTTP requests.
#
handler = http.server.SimpleHTTPRequestHandler

#
#  Create socket server at will connect the HTTP handler
#  to the low level TCP port.
#
tcpServer = socketserver.TCPServer(("", PORT), handler)

#
#  Start the server.
#
print("serving at http://localhost:{}".format(PORT))
tcpServer.serve_forever()

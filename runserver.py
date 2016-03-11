#!/usr/bin/env python
from arborist import app
import socket
import argparse
import webbrowser

parser = argparse.ArgumentParser(description='Launch the Arborist')
parser.add_argument('--debug', action="store_true", default=False, help="Run in debug mode")
parser.add_argument('--port', type=int,
                    help="Set port try to run on. In the case of socket error another is tried.")
args = parser.parse_args()


def get_open_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port

if not args.port:
    port = get_open_port()
else:
    port = args.port

running_on = 'http://localhost:{}'.format(port)
webbrowser.open(running_on, new=0, autoraise=True)
app.run(debug=args.debug, port=port)

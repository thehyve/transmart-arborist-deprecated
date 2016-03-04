#!/usr/bin/env python
from arborist import app
import socket
import argparse

parser = argparse.ArgumentParser(description='Launch the Arborist')
parser.add_argument('--debug', action="store_true", default=False, help="Run in debug mode")
parser.add_argument('--port', default=5000, help="Set port to run on.")
args = parser.parse_args()


for port in range(1024, 64000):
    print('Trying port: ' + str(port))
    try:
        app.run(debug=args.debug, port=port)
        break
    except socket.error:
        print('Failed. Trying next:')

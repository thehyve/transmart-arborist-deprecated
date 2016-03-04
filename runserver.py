#!/usr/bin/env python
from arborist import app
import argparse

parser = argparse.ArgumentParser(description='Launch the Arborist')
parser.add_argument('--debug', action="store_true", default=False, help="Run in debug mode")
args = parser.parse_args()

app.run(debug=args.debug)

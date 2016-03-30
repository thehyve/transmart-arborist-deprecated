from arborist import app
import socket
import argparse
import webbrowser

parser = argparse.ArgumentParser(description='Launch the Arborist')
parser.add_argument('--debug', action="store_true", default=False, help="Run in debug mode")
parser.add_argument('--port', type=int,
                    help="Set port to try to listen to. By default the OS is asked what port to use.")
parser.add_argument('--path', default=None, dest='initial_path',
                    help="Set a path to a column mapping file, to load the tree editing mode directly.")
args = parser.parse_args()


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    s.listen(1)
    available_port = s.getsockname()[1]
    s.close()
    return available_port

if not args.port:
    port = get_open_port()
else:
    port = args.port

if not args.debug:
    running_on = 'http://localhost:{}'.format(port)
    if args.initial_path:
        running_on += '/folder/' + args.initial_path
    webbrowser.open(running_on, new=0, autoraise=True)

app.run(debug=args.debug, port=port)

import http.server
import socketserver
import xml.etree.ElementTree as ET
from string import Template
import argparse
from pathlib import PurePath

parser = argparse.ArgumentParser(
    description="Build and serves a VR page for a 3d model, with automatic path following."
)
parser.add_argument("fname", type=str, help="Input 3d model file")
parser.add_argument(
    "path",
    type=str,
    default="model_picked_points.pp",
    help="Picked points file for path along the model (default: model_picked_points.pp)",
)
parser.add_argument("duration", type=int, help="Duration of the path in seconds")
parser.add_argument(
    "--scale",
    type=float,
    default=1.0,
    help="Scaling factor for the model (default: 1.0)",
)
parser.add_argument(
    "--height",
    type=float,
    default=10.0,
    help="Height of the camera above the path (default: 10.0)"
)
parser.add_argument(
    "--serve",
    action="store_true",
    help="Serves the file using python's builtin http server"
)

args = parser.parse_args()

tree = ET.parse(args.path)
points = {}
for x in tree.getroot().findall("./point"):
    points[int(x.attrib["name"])] = (
        float(x.attrib["x"]) * args.scale,
        float(x.attrib["y"]) * args.scale,
        float(x.attrib["z"]) * args.scale,
    )

points = [list(points[key]) for key in sorted(points.keys())]

with open("index_template.html") as fin, open("index.html", "w") as fout:
    fout.write(
        Template(fin.read()).substitute(
            model_file=PurePath(args.fname).as_posix(),
            camera_path=" ".join([f"{p[0]},{p[1]},{p[2]}" for p in points]),
            time_length=args.duration*1000,
            model_scale=args.scale,
            height=args.height
        )
    )

# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# s.close()

if args.serve:
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving model at port", PORT)
        httpd.serve_forever()

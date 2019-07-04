# aframe-path
A really simple vr view following a given path using a-frame

```
usage: python model_viewer.py [-h] [--scale SCALE] [--height HEIGHT] [--serve]
                       fname path duration

Build and serves a VR page for a 3d model, with automatic path following.

positional arguments:
  fname            Input 3d model file
  path             Picked points file for path along the model (default:
                   model_picked_points.pp)
  duration         Duration of the path in seconds

optional arguments:
  -h, --help       show this help message and exit
  --scale SCALE    Scaling factor for the model (default: 1.0)
  --height HEIGHT  Height of the camera above the path (default: 10.0)
  --serve          Serves the file using python's builtin http server
```
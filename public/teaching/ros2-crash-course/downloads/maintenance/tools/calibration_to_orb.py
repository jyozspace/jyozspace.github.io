"""Convert ROS monocular plumb_bob calibration to an ORB-SLAM3 settings file.

Needs python3-yaml. Never substitutes a guessed camera calibration.
"""
import argparse
import math
from pathlib import Path
import yaml


def convert(c, fps):
    k = c['camera_matrix']['data']
    d = list(c['distortion_coefficients']['data'])
    width, height = c['image_width'], c['image_height']
    if c['distortion_model'] != 'plumb_bob' or len(d) not in (4, 5):
        raise ValueError('Only 4/5-coefficient plumb_bob is supported by this converter')
    if len(k) != 9 or not all(math.isfinite(float(v)) for v in k+d):
        raise ValueError('Malformed calibration matrices')
    if width <= 0 or height <= 0 or k[0] <= 0 or k[4] <= 0 or not 1 <= fps <= 30:
        raise ValueError('Invalid dimensions, focal length or nominal frame rate')
    d += [0.0] * (5-len(d))
    values = {'File.version': '"1.0"', 'Camera.type': '"PinHole"',
              'Camera1.fx': k[0], 'Camera1.fy': k[4], 'Camera1.cx': k[2], 'Camera1.cy': k[5],
              'Camera1.k1': d[0], 'Camera1.k2': d[1], 'Camera1.p1': d[2], 'Camera1.p2': d[3], 'Camera1.k3': d[4],
              'Camera.width': width, 'Camera.height': height, 'Camera.fps': fps, 'Camera.RGB': 0,
              'ORBextractor.nFeatures': 1200, 'ORBextractor.scaleFactor': 1.2, 'ORBextractor.nLevels': 8,
              'ORBextractor.iniThFAST': 20, 'ORBextractor.minThFAST': 7,
              'Viewer.KeyFrameSize': 0.05, 'Viewer.KeyFrameLineWidth': 1, 'Viewer.GraphLineWidth': 0.9,
              'Viewer.PointSize': 2, 'Viewer.CameraSize': 0.08, 'Viewer.CameraLineWidth': 3,
              'Viewer.ViewpointX': 0, 'Viewer.ViewpointY': -0.7, 'Viewer.ViewpointZ': -1.8, 'Viewer.ViewpointF': 500}
    return '%YAML:1.0\n# Generated from measured ROS calibration; images are BGR.\n'+''.join(f'{key}: {value}\n' for key,value in values.items())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--fps', type=float, default=10)
    args = parser.parse_args()
    args.output.write_text(convert(yaml.safe_load(args.input.read_text()), args.fps))
    print('Wrote measured calibration for ORB-SLAM3:', args.output)

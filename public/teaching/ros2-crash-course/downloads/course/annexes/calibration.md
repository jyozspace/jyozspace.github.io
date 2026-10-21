# Annex C: camera and IMU calibration

Calibration measures how sensor numbers relate to geometry, units and time. For the core capstone, complete the camera workflow and inspect the native motion components. Camera–IMU fusion is a further project requiring a sensor source with suitable timing and calibration support. Allow 45–90 minutes for a first camera session; qualify the phone before the live mapping lecture.

## Separate four questions

| Question | Quantity | Required for the supplied monocular mapper? |
| --- | --- | --- |
| Where does an image pixel point? | Camera intrinsics and lens distortion | Yes |
| How are the camera and IMU mounted? | Relative rotation and translation, called extrinsics | Needed for future inertial fusion |
| When was each measurement taken? | Clock relation, exposure/sample time and temporal offset | Consistent image times now; qualified camera–IMU timing for fusion |
| How uncertain are inertial values? | Bias, noise density and bias random walk | Needed for future inertial fusion |

A visible checkerboard solves the first question. It cannot by itself supply inertial noise or guarantee simultaneous camera/IMU samples. The [OpenVINS calibration guide](https://docs.openvins.com/gs-calibration.html) explains how these quantities fit an estimator.

## Prepare the exact transmitted camera mode

For Android, record the displayed rear camera ID, native YUV dimensions, sensor orientation, focus mode and camera clock source. The app sends unrotated JPEGs of those pixels and requests stabilization off. Hold one orientation and use the same mode for calibration and mapping. A calibration measures the transmitted stream’s pixel geometry, so changing camera or image processing requires a fresh measurement or validated conversion. USB and wireless transport preserve the same pixels and use the same calibration when the camera mode stays fixed.

Print a checkerboard on a flat rigid backing. Count **inner corners**, where four squares meet: a board with 9×7 squares has 8×6 inner corners. Measure a square edge on the final print, since printer scaling can change it. In this example each square is 24 mm, so the tool receives 0.024 metres. Use your own measured values.

![Simulated calibration view: a 9-by-7 square target has 8-by-6 inner corners. Coverage bars represent varied position, size and tilt.](../assets/calibration-screen.svg)

## Collect coverage, calibrate and save

Start the uncalibrated bridge and stream the chosen camera mode. In another sourced terminal:

```bash
ros2 run camera_calibration cameracalibrator \
  --size 8x6 --square 0.024 --no-service-check \
  --ros-args -r image:=/phone/camera/image_raw -r camera:=/phone/camera
```

Move the target slowly through the image: center and edges, near and far, then tilted about different axes. Keep the whole board visible for useful samples. The X/Y/Size/Skew indicators help you collect varied views. Sharp, well-lit images help corners be detected accurately. If detection fails, inspect inner-corner counts, glare, blur and target flatness first.

When coverage is sufficient, choose **Calibrate**, inspect the result and then **Save**. The standard tool normally writes /tmp/calibrationdata.tar.gz. List its contents, locate the monocular YAML and copy that file to ~/phone-lab/camera.yaml. Save works with this receiver; Commit would require a set_camera_info service that the supplied bridge does not expose.

```bash
tar -tzf /tmp/calibrationdata.tar.gz
mkdir -p ~/phone-lab/calibration-export
tar -xzf /tmp/calibrationdata.tar.gz -C ~/phone-lab/calibration-export
find ~/phone-lab/calibration-export -name '*.yaml'
```

Use the path printed by find for the following copy; replace EXPORTED_YAML with that path:

```bash
cp EXPORTED_YAML ~/phone-lab/camera.yaml
```

Follow the official [monocular calibration tutorial](https://docs.ros.org/en/jazzy/p/camera_calibration/doc/tutorial_mono.html) for tool controls and [its Jazzy implementation](https://github.com/ros-perception/image_pipeline/tree/jazzy/camera_calibration) for version-specific options. Coverage is necessary, while a low reprojection error is only one diagnostic: evaluate the fit on fresh views too.

## Interpret and validate the saved model

The pinhole matrix K is [fx, 0, cx; 0, fy, cy; 0, 0, 1]. Focal lengths fx/fy and principal point cx/cy are in pixels. D contains distortion coefficients; their number and meaning depend on distortion_model. R and P support rectification/projection conventions. Read the YAML’s image_width and image_height and compare them with the actual topic. CameraInfo documents each field.

Restart the bridge with --calibration ~/phone-lab/camera.yaml. Inspect one CameraInfo message and a fresh live image. Check that dimensions match, K has positive focal lengths, and the optical axes refer to the transmitted image. Validate rectification on separate target views using the image_pipeline tools: straight target edges should become more consistent with the selected lens model. Repeat calibration if the fit or camera mode is unstable.

For the optional mapper, run the converter from the unpacked backend/source folder:

```bash
python3 maintenance/tools/calibration_to_orb.py \
  ~/phone-lab/camera.yaml ~/phone-lab/phone-orb.yaml --fps 10
```

The converter supports measured pinhole plumb_bob models with four or five distortion coefficients. It translates file formats; it does not estimate new values. A different distortion model needs an appropriate converter and estimator model. Retain the original YAML, target measurements, actual frame rate, image dimensions and source revisions with the recording. See [OpenCV’s camera model](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) for the projection equations.

## Inspect the IMU before planning fusion

Hold the phone still, then rotate it slowly about one device axis at a time. Echo /phone/imu/gyroscope and record which angular component responds and with which sign. Echo /phone/imu/accelerometer separately to inspect acceleration. At rest the gyroscope should be close to zero, while the magnitude of acceleration including gravity is often near 9.8 m/s². Record the phone orientation and compare signs with Android’s device-axis definition. The camera optical axes describe the unrotated transmitted image and need a measured extrinsic relationship to the device axes.

![Illustrative IMU inspection checklist: stationary values and one-axis rotations test units and signs, while physical camera–IMU calibration remains a separate measurement.](../assets/imu-check.svg)

Collect a short stationary recording and plot all six components. Look for missing values, irregular intervals, saturation and obvious bias. A stationary mean is an observation under those conditions; the API’s sensor calibration/filtering and actual timing quality limit what can be inferred from it. Native events retain separate accelerometer/gyroscope times. REALTIME camera timestamps share their phone clock domain, while UNKNOWN camera devices use this app’s labelled image callback fallback. The bridge marks orientation unavailable and leaves unknown covariance explicit. Use the [Imu message contract](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/Imu.html) when describing this data.

## Plan a camera–IMU calibration project

For qualified inertial fusion, first choose a native/hardware sensor source with known image and IMU timestamps, a stable camera model and a supported estimator. Preserve the raw streams and metadata. Then follow a documented calibration pipeline such as the [Kalibr project’s camera–IMU procedure](https://github.com/ethz-asl/kalibr/wiki/camera-imu-calibration) and [IMU noise model](https://github.com/ethz-asl/kalibr/wiki/IMU-Noise-Model).

1. Calibrate camera intrinsics in the acquisition mode and prepare the calibration target definition.
2. Characterize inertial noise and bias using the pipeline’s specified stationary acquisition and analysis procedure. This commonly needs much longer data than a classroom motion demo.
3. Capture joint camera/IMU data with the target visible and varied, smooth rotation and translation that excite all axes.
4. Estimate the rigid camera–IMU transform and temporal offset using the chosen tool. Read its transform direction and time-offset sign convention before conversion.
5. Inspect residuals, coverage and repeatability; validate the model on a different sequence before running visual-inertial estimation.

Kalibr has its own supported input/environment requirements. Plan ROS 2 bag conversion and the alignment of independently timestamped accelerometer/gyroscope streams explicitly, preserving original samples. Check REALTIME camera metadata, exposure/readout and residual timing on the actual phone. A constant-offset estimate cannot repair an unknown time-varying delay. The provided mapper keeps the core course focused on monocular images, while native component topics support this further calibration project.

## Submit a reproducible calibration record

Include the target dimensions and measured square size, phone/app/camera ID/mode, transmitted image dimensions, original YAML, converted settings, coverage and validation evidence, and the changes that would invalidate this calibration. Explain what you checked about the IMU and which quantities remain unknown. A strong report separates measured quantities from assumptions and proposed future work.

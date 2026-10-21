# Frames: where a measurement lives

A coordinate frame is a named origin and three directed axes. A point's coordinates are meaningful only relative to that frame. A timestamp says when the measurement or transform applies. Names and timestamps are part of the data contract, not decorative labels.

## Start with a physical picture

Imagine the phone upright and its camera looking at a mug. In a camera optical frame, x points right in the transmitted image, y down and z forward through the lens. A visible mug is usually at positive z. Its pixel location is not itself a 3D point: one image pixel identifies a viewing ray, and depth is still unknown.

ROS body frames conventionally use x forward, y left, z up. Android sensor axes are defined relative to the device’s natural orientation. The camera optical frame describes the transmitted pixels; its mounting and axis relationship to either motion frame must be measured. A screen rotating does not physically rotate the camera mounting, but it may change the image presentation. That is why the project keeps a fixed orientation and calibrates the exact image stream.



![Transform ownership and a point calculation: a positive 90-degree yaw rotates sensor x toward base y.](../assets/tf-tree.svg)

## Transform a point, step by step

A rigid transform contains a rotation R and translation t. The notation **T_A_B** here maps coordinates expressed in B into A: p_A = R_A_B p_B + t_A_B. The translation is B's origin expressed in A, and the rotation maps B's axes into A. This convention must be stated; different libraries use different symbols.

Suppose a range sensor is mounted 0.1 m forward and 0.2 m above a base, with parallel axes. A measured point p_sensor = (1, 0, 0) m becomes p_base = (1.1, 0, 0.2) m. Merely changing its frame_id to base_link would leave the numbers unchanged and create a false measurement.

If the sensor is also yawed +90° about the base's z axis, its positive x points along the base's positive y. The same point becomes (0.1, 1.0, 0.2) m. Rotation and translation do different jobs. Use the numeric transform lab in lecture 4 to try this example before calculating it by hand.

## Compose and invert carefully

For a chain A → B → C, **T_A_C = T_A_B T_B_C**. Apply the rightmost transform first. Matrix order matters: rotating and then translating generally differs from translating and then rotating. With homogeneous coordinates, each rigid transform is a 4×4 matrix with R in the upper-left, t in the final column and [0,0,0,1] as the last row.

For the inverse, transpose R and calculate the translation as -R transpose times t. This follows from reversing both the rotation and translation. Quaternions encode rotation as x, y, z, w in ROS messages. A valid rotation quaternion must have unit norm. Identity is (0,0,0,1), not four zeros. Euler angles are convenient for small examples but require a stated axis/order convention and can have singularities.

## Know what TF publishes

In TF notation, a parent frame and child frame identify a relative pose. The translation gives the child origin in parent coordinates. In a Python lookup, `lookup_transform(target, source, time)` returns the transform that maps source coordinates into target coordinates. This target/source order is a common beginner mistake.

Each child should have one parent and one authoritative publisher at a time. TF is a tree, not a collection of contradictory estimates. A static transform describes a fixed calibrated mounting and is retained on /tf_static. A dynamic transform changes with time and is sent on /tf. CameraInfo describes projection and calibration; it does not create either TF topic.

```bash
ros2 run tf2_ros static_transform_publisher \
  --x 0.1 --y 0.0 --z 0.2 --roll 0 --pitch 0 --yaw 1.57079632679 \
  --frame-id demo_base --child-frame-id demo_sensor
```

In another sourced terminal:

```bash
ros2 run tf2_ros tf2_echo demo_base demo_sensor
ros2 run tf2_tools view_frames
```

Expected: translation (0.1,0,0.2) and a rotation of about +90° around z. These are teaching values for demo frames, not your phone's camera–IMU calibration. Stop the demonstration publisher after the exercise.

## Separate global and local motion

For a metric mobile robot, a common chain is map → odom → base_link → camera_link → camera_optical_frame. Local odometry supplies odom → base_link continuously but may drift. Global mapping/localization supplies map → odom to correct drift; that correction can jump after a loop closure. Calibration or robot description supplies the rigid sensor chain.

The phone project's monocular world is deliberately named phone_slam_world. Its scale and gravity direction are not known from the camera alone. Publishing its arbitrary coordinates into a metre-valued robot TF tree would imply a physical calibration that has not been established. The optional adapter therefore publishes stamped poses/clouds for visualization in its own visualization frame, preserving the distinction between estimated reconstruction and measured physical geometry.

## Match time as well as geometry

A correct frame tree can still fail at the measurement's time. TF keeps a finite history. Asking for data older than the buffer, later than available transforms, or using a wall-time stamp against replay time can cause extrapolation errors. A latest-transform lookup may be acceptable for inspection, but it is not a general substitute for transforming a measurement at its actual timestamp.

For Android, bridge stamps convert SensorEvent times and REALTIME camera times into the laptop clock; UNKNOWN camera sources use a labelled callback estimate. The phone-to-laptop offset is approximate. For bag replay, /clock and use_sim_time make consumers use recorded ROS time. Slower replay changes wall-time pacing, not the recorded geometry or timestamps. If your phone IMU/camera relation is unknown, a time fix alone does not establish extrinsic calibration.

## Check your explanation

Explain where the point (1,0,0) goes under the +90° demo transform; which node should own odom → base_link on a moving robot; why renaming frame_id is not a transform; and why a received IMU message does not prove that its axes match the phone camera. A good answer specifies frames, units, transform direction and time.

Sources: [REP 103](https://www.ros.org/reps/rep-0103.html), [REP 105](https://www.ros.org/reps/rep-0105.html), [Jazzy TF2 tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html), [OpenVINS sensor calibration](https://docs.openvins.com/gs-calibration.html).

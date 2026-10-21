# A custom message describing the state of a (pretend) robot.
# Field types come from the built-in ROS 2 IDL types:
#   bool, byte, char, float32, float64, int8/16/32/64, uint8/16/32/64, string
# Arrays: int32[] unbounded, int32[5] fixed, int32[<=5] bounded

string  robot_name        # human readable name, e.g. "tb3_01"
float32 battery_percent   # 0.0 .. 100.0
bool    is_moving         # true while wheels are turning
uint8   fault_code        # 0 = OK

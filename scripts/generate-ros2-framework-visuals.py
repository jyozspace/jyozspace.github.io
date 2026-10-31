"""Draw lecture 01's framework diagrams as editable, course-palette SVGs."""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[1] / 'public/teaching/ros2-crash-course/assets'
BG, PAPER, INK, MUTED = '#f6f5f0', '#fffefa', '#1b3634', '#6a7771'
GREEN, LIME, WASH, COPPER, LINE = '#235c4b', '#d4edab', '#eaf0e5', '#b96d3f', '#dce1d7'


def text(x, y, value, size=24, fill=INK, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'


def rect(x, y, w, h, fill=PAPER, stroke=LINE, radius=16):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def path(d, color=GREEN, arrow=False, dash=False):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="7 8"' if dash else '')+'/>'


def card(x, y, w, title, sub, number=None, h=92, fill=PAPER):
    s = rect(x, y, w, h, fill)
    if number:
        s += f'<circle cx="{x+32}" cy="{y+34}" r="17" fill="{WASH}"/>'+text(x+32,y+40,number,17,GREEN,700,'middle')
    start = x+62 if number else x+22
    return s+text(start,y+37,title,25,INK,700)+text(x+22,y+h-23,sub,21,MUTED)


def document(name, title, description, h, body):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{GREEN}"/></marker></defs>
<g font-family="Inter, Segoe UI, Arial, sans-serif"><rect width="1200" height="{h}" fill="{BG}"/>
{text(48,43,'NODES TO MAPS  /  ROS 2 FOUNDATIONS',16,COPPER,700)}
{text(48,102,title,43,INK,700)}
{body}
{path(f'M48 {h-47}H1152',LINE)}
{text(48,h-19,'CONCEPT DIAGRAM · CC BY 4.0 · NODES TO MAPS',14,MUTED)}
</g></svg>'''
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/name).write_text(svg, encoding='utf-8')


def shared_interfaces():
    b = text(48,140,'Agree on the interface once. Connect independent consumers.',23,MUTED)
    b += rect(48,170,1104,202)+text(72,204,'CUSTOM CONNECTIONS',17,COPPER,700)
    for x,title,sub in [(72,'Camera','pixels'),(344,'Detector','objects'),(616,'Planner','path'),(888,'Controller','wheel commands')]:
        b += card(x,225,240,title,sub,h=96)
    for x in [312,584,856]:
        b += path(f'M{x+3} 273H{x+28}',COPPER)
    b += text(72,350,'Every boundary needs agreement on formats, units, timing and configuration.',22,MUTED)
    b += rect(48,398,1104,370,WASH)+text(72,436,'SHARED ROS INTERFACES',17,GREEN,700)
    for y,title,sub in [(466,'Real camera','driver'),(558,'Simulation','sensor model'),(650,'Recorded bag','replay')]:
        b += card(72,y,214,title,sub,h=82)
        b += path(f'M286 {y+41}H328V599H366',arrow=True)
    b += rect(366,510,386,178,GREEN,GREEN)
    b += text(559,553,'ONE TYPED STREAM',18,LIME,700,'middle')
    b += text(559,596,'/camera/image_raw',28,PAPER,700,'middle')
    b += text(559,637,'sensor_msgs/msg/Image',24,PAPER,400,'middle')
    for y,title,sub in [(466,'RViz','view images'),(558,'rosbag2','record images'),(650,'Vision node','process images')]:
        b += path(f'M752 599H793V{y+41}H834',arrow=True)
        b += card(834,y,294,title,sub,h=82)
    b += text(48,810,'Choose a source; reuse consumers. Match encoding, timestamps, calibration and QoS.',23,GREEN,600)
    document('lecture01-shared-interfaces.svg','Shared interfaces reduce custom glue',
             'Custom links between a camera, detector, planner and controller are compared with interchangeable image sources feeding one ROS topic and independent RViz, rosbag2 and vision subscribers.',880,b)


def toolbox():
    b = text(48,140,'Combine reusable capabilities around your own application.',23,MUTED)
    items = [(48,180,'Visualize','RViz','Inspect live sensor data.'),
             (48,374,'Record & replay','rosbag2','Repeat an experiment.'),
             (48,568,'Simulate','Gazebo','Model physics and sensors.'),
             (832,180,'Navigate','Nav2 + localization','Plan and follow paths.'),
             (832,374,'Move an arm','MoveIt','Plan manipulation motions.'),
             (832,568,'Connect hardware','Drivers + ros2_control','Read sensors; command hardware.')]
    for x,y,_,_,_ in items:
        b += path(f'M600 451H{(420 if x==48 else 780)}V{y+74}H{(368 if x==48 else 832)}',dash=True)
    b += rect(448,297,304,310,GREEN,GREEN)
    # A deliberately simple original robot silhouette.
    b += rect(527,355,146,113,PAPER,PAPER,24)
    b += '<circle cx="565" cy="396" r="10" fill="'+GREEN+'"/><circle cx="635" cy="396" r="10" fill="'+GREEN+'"/>'
    b += path('M569 435H631',COPPER)+path('M600 355V332',PAPER)
    b += f'<circle cx="600" cy="325" r="7" fill="{LIME}"/>'
    b += text(600,523,'YOUR ROBOT',28,PAPER,700,'middle')+text(600,558,'your application logic',22,LIME,400,'middle')
    for i,(x,y,title,pkg,sub) in enumerate(items):
        b += rect(x,y,320,152)+text(x+22,y+36,title,27,INK,700)
        b += text(x+22,y+77,pkg,24,GREEN,600)+text(x+22,y+118,sub,19,MUTED)
    b += rect(48,754,1104,92,WASH)
    for x,head,sub in [(72,'Shared interfaces','Typed messages + conventions'),(446,'Python + C++','Nodes can work together'),(818,'One or many computers','Reachable, configured peers')]:
        b += text(x,789,head,23,GREEN,700)+text(x,820,sub,20,MUTED)
    b += text(48,891,'Select compatible packages; supply the robot model, drivers, configuration and hardware.',22,MUTED)
    document('lecture01-reuse-toolbox.svg','Reuse the plumbing. Focus on the robot.',
             'Six reusable software capabilities surround a robot application: visualization, recording, simulation, navigation, manipulation and hardware integration. Shared interfaces let compatible Python and C++ nodes work on one or several computers.',960,b)


def dds_network():
    b = text(48,140,'DDS implementations discover endpoints and exchange compatible typed samples.',23,MUTED)
    nodes=[(48,'Sensor drivers','Camera · lidar · IMU'),(432,'Localization','Estimate the robot pose'),(816,'Planning','Compute a route')]
    for x,title,sub in nodes:
        b += card(x,190,336,title,sub,h=115)
        b += path(f'M{x+168} 305V370',arrow=True)
    b += rect(48,373,1104,163,GREEN,GREEN)
    b += text(600,417,'SHARED TOPIC DATA SPACE',22,LIME,700,'middle')
    for x,w,label in [(93,266,'/camera/image_raw'),(387,174,'/scan'),(589,150,'/tf'),(767,338,'/cmd_vel')]:
        b += rect(x,445,w,58,PAPER,PAPER,10)+text(x+w/2,482,label,25,GREEN,600,'middle')
    for x,title,sub in [(48,'Visualization','RViz inspects data'),(432,'Navigation & control','Follow a path; command motors'),(816,'Recording','rosbag2 saves streams')]:
        b += path(f'M{x+168} 536V600',arrow=True)
        b += card(x,602,336,title,sub,h=115)
    b += text(48,760,'The band groups logical data paths. It is not a central DDS server or a physical bus.',23,COPPER,600)
    b += rect(48,792,1104,158,WASH)
    b += text(72,830,'INSIDE EACH ROS PROCESS',17,GREEN,700)
    b += text(72,868,'Node → rclpy / rclcpp → RMW → DDS implementation → OS transport',25,INK,600)
    b += text(72,909,'Discover peers first; then match topic names, types and QoS before exchanging data.',22,MUTED)
    b += text(48,990,'Nodes can publish and subscribe. Arrows show example roles, not every connection.',22,MUTED)
    document('lecture01-dds-network.svg','DDS connects a distributed ROS graph',
             'Sensors, localization and planning share topic data with visualization, navigation/control and recording. The shared band is a conceptual data space, not a centralized server. Each process uses ROS client libraries, RMW, a DDS implementation and OS transport.',1060,b)


if __name__ == '__main__':
    shared_interfaces()
    toolbox()
    dds_network()
    print('Created three course-palette lecture 01 SVG diagrams.')

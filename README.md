# DAIR-Perception

Welcome to the official QMIND DAIR-Perception Team!  
<br>
Our goal was to design an enhanced robot perception system that supports computer vision and deep
learning to aid in autonomous driving . With real-time object detection, our software controls a
Turtlebot3 to correctly navigate and seek out specified objects in a room. The system implements Simultaneous
Localization and Mapping (SLAM) with LiDAR & camera sensing to improve object detection in dynamic environments.
As part of QMIND's Division of AI Research (DAIR), exploration and development on new methods for custom datasets,
deep neural networks, robot operation and control systems were vital to developing an efficient end-to-end machine learning system.

## Team Members:
Sam Cantor - Project Manager<br>
Ted Ecclestone - Control Systems Specialist<br>
Adam Cooke - Algorithm Specialist<br>
Buchi Maduekwe - Data Specialist<br>
Tanner Dunn - Data Specialist<br> 

## YOLOv3 ROS
Part of our project included developing our own library to detect objects from images in ROS through nodes. This way, 
robots can publish image feeds for the computer to subscribe to and process, cutting down on the computational load 
for the raspberry pi. We used YOLOv3 as our object detection model, and developed it such that any robot can easily modify 
and scale this solution for any problem. If you are interested in using our library or exploring how it works, we made a 
smaller repo that only includes the object detection code, check it out [here](https://github.com/sjcantor/YOLOv3-ROS)!


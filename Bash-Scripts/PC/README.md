# PC Bash Scripts
These are a few simple bash scripts developed by the team to make some of the setup easier.  
<br>
### Install Steps:  
- Navigate to home directory using command `cd ~`  
- Create a new directory "bin" using `mkdir bin`  
- Navigate to directory using `cd bin` and place bash scripts inside  
- Make scripts executable by running command `chmod +x [name of script]`  
<br><br>
### Usage:  
From any directory... 
```
[name of command]
Ex:
run-rviz
```
## start-image-view
This will run the object detection model through the Turtlebot camera, and publish a stream of compressed images containing the predicted bounding boxes. Process can be exited using `stop-image-view`
#### Run these first:
* roscore
* bringup (pi)
* camera (pi)
* run-rviz *(recommended)*
<br><br>
## start-movement
Will launch the movement script, subscribes to the object-detection output and implements a navigation algorithm to locate and approach an object of choice. Can be exited using `stop-movement`
<br>
## run-rviz
Runs relevant commands to load the turtlebot in Rviz. Make sure to have [PC] `roscore` and [Pi] `./bringup.sh` running in separate terminals first.
<br>
## run-teleop
Enables teleoperation for the turlebot using arrow keys on laptop. Previous steps apply.
<br>
## gits
Runs command `git status`, but with less characters needed. A simple but effective script for lazy programmers.

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

## run-rviz
Runs relevant commands to load the turtlebot in Rviz. Make sure to have [PC] `roscore` and [Pi] `./bringup.sh` running in separate terminals first.

## run-teleop
Enables teleoperation for the turlebot using arrow keys on laptop. Previous steps apply.

## gits
Runs command `git status`, but with less characters needed. A simple but effective script for lazy programmers.

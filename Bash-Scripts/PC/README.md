# PC Bash Scripts
These are a few simple bash scripts developed by the team to make some of the setup easier.  
<br>
Install Steps:  
- Navigate to home directory using command `cd ~`  
- Create a new directory "bin" using `mkdir bin`  
- Navigate to directory using `cd bin` and place bash scripts inside  
- Make scripts executable by running command `chmod +x [name of script]`  
<br>
Usage:  <br>
From any directory:  <br>
```
[name of command]
Ex:
run-rviz
```

## run-rviz
Runs relevant commands to load the turtlebot in Rviz. Make sure to have [PC] `roscore` and [Pi] `./bringup.sh` running in separate terminals first.
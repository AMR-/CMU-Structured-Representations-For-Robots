
This folder contains the code to support running the Interactive TAIG demo described in Chapter 4 of the thesis.  Of course, it requires a Pepper robot.

Run it in a python environment where you have pip-installed `instruction-graph` and where you can `import qi` for communicating with Pepper.

This particular code will not work without a Pepper robot, although you can inspect it and apply the principles to use interactive-TAIG in other projects.

A few additional notes:

To run, run 

    python itaig_demo.py --ip [ip.of.your.pepper]

This particular script has a timeout of 1000 seconds, this can be modified on line 45.  Saying "thank you" or "Stop" to the robot will also end the script gracefully.

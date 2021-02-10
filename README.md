# Gradient Descent Pathing Algorithm Demo

This program is a demonstration of the gradient descent algorithm for pathing around obstacles in a 3D environment. It uses VPython to display 3D graphics and NumPy for matrix calculations. Implementation done in **Python 3.8.7**, no other versions tested.

#### To run from directory
1. Install requirements with "pip install -r requirements.txt"
2. Run "python animation.py"

#### Program use
1. The program will set up the inital scene based on lists *cyl_pts* and *ball_pts* (Note: Bind the function **print_pos** to a click event to test cylinder positions)
2. The program is hard coded to generate 6 balls, but this can be adjusted by adding the proper number of color values to the *colors* list along side updates to *ball_pts*
3. After initial set up, click anywhere in the bounds defined by the white rectangle to have all balls path towards it
4. When a ball reaches the goal, it will stop and wait for the other balls to arrive
5. The program will loop until all balls reach the goal (Note: Program status will be shown in a caption below the scene)
6. The goal can be dynamically changed both while pathing and while stationary

#### Known issues
1. Balls may get stuck if the goal is placed too close to an obstacle that directly blocks its path
2. Balls are repelled by eachother, which can make all balls reaching the goal difficult (Note: Place a new goal between the balls until the status is no longer pathing)
3. Placing obstacles too close to eachother will result in local maxima that balls will not be able to path through

#### References: 
Algorithm: *Cost Minimization for Animated Geometric Models in Computer Graphics* by David E. Breen
Documentation for Vpython: https://www.glowscript.org/docs/VPythonDocs/index.html
Documentation for NumPy: https://numpy.org/doc/

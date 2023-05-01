# python_movement_tracking
movement based tracking in Python with OpenCV

The tracking in this program is achieved by background subtraction on each frame.
Once the background is subtracted, the largest contour is found, the centroid of it
is calculated, and that is assumed to be the center of the object.

25/04/23 - added functionality to run the auditory looming test (ALT) 
This test is to measure defensive responses to sounds that mimic an approaching object. 
ALT sound levels can be adjusted by running the calibrate.py script.

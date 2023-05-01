'''
should you change the return values to strings that just say the location?
'''

import cv2
import numpy as np

def pointInside(frame, rectangle, p, time):
    # Draw rectangle on the frame
    # Draw red rectangle if rect does not contain point
    # prevState = False

    x,y,w,h = rectangle
    px, py = p

    if (x <= px <= x+w and y <= py <= y+h):
    # if not rectangle.contains(p):
        cv2.rectangle(frame, rectangle, (0, 0, 255), 2)
        # prevState = False

        # When habituation is done, show that the trigger is on
        if time > 600:
            cv2.putText(frame, "STIM ON", (10,frame.shape[0]-10), cv2.FONT_HERSHEY_DUPLEX, 2.0, (118, 185, 0), 2)
            print("stimulus triggered")

        # print("point is in the square")
        # cv2.putText(frame, "STIM ON", (10, frame.shape[0] // 10), cv2.FONT_HERSHEY_DUPLEX, 2.0, (118, 185, 0), 2)
        return "TRIGGER"
     
    # Draw green rectangle if rect contains point
    else:
        cv2.rectangle(frame, rectangle, (0, 255, 0), 2)
        # print("point is in the connector")
        # cv2.putText(frame, "STIM OFF", (10, frame.shape[0] // 10), cv2.FONT_HERSHEY_DUPLEX, 2.0, (118, 185, 0), 2)
        return "NONE"

        # use if statement play sound

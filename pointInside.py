import cv2
import numpy as np

def pointInside(frame, rectangle, p):
    # Draw rectangle on the frame
    # Draw red rectangle if rect does not contain point
    prevState = False

    x,y,w,h = rectangle
    px, py = p

    if not (x <= px <= x+w and y <= py <= y+h):
    # if not rectangle.contains(p):
        cv2.rectangle(frame, rectangle, (0, 0, 255), 2)
        prevState = False

        if px < x:
            # print("point is in the square")
            cv2.putText(frame, "TRIANGLE", (10, frame.shape[0] // 10), cv2.FONT_HERSHEY_DUPLEX, 2.0, (118, 185, 0), 2)
            return 0
        if px > (x + w):
            # print("point is in the triangle")
            cv2.putText(frame, "SQUARE", (10, frame.shape[0] // 10), cv2.FONT_HERSHEY_DUPLEX, 2.0, (118, 185, 0), 2)
            return 1

    # Draw green rectangle if rect contains point
    else:
        cv2.rectangle(frame, rectangle, (0, 255, 0), 2)
        # print("point is in the connector")
        cv2.putText(frame, "CONNECTOR", (10, frame.shape[0] // 10), cv2.FONT_HERSHEY_DUPLEX, 2.0, (118, 185, 0), 2)
        return 2

        # use if statement play sound

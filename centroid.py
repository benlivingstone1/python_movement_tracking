import cv2
import numpy as np

def centroid(fgndMask):
    # Find all the contours in the image
    contours, hierarchy = cv2.findContours(fgndMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Sort the contours in descending order
    # contours(sorted(key=lambda c: cv2.contourArea(c), reverse=True))
    # contours = sorted(contours, reverse=True)

    contour_area = []
    for c in contours:
        contour_area.append(cv2.contourArea(c))

    contour_area = sorted(contour_area, reverse=True)

    try:
        largest_contour = max(contours, key=cv2.contourArea)
    except ValueError:
        largest_contour = None

    if largest_contour is not None:
        # Calculate the moments of the largest contour
        m = cv2.moments(largest_contour)
        p = (m['m10'] / (m['m00'] + 1e-5), m['m01'] / (m['m00'] + 1e-5))

        return p
    else:
        p = (0,0)
        return p

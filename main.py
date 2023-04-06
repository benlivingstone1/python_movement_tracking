import cv2
import numpy as np
import imgProc
import centroid
import csv
import pointInside

# Create a video capture object:
# Put a filename as argument, otherwise "0" opens default camera
video = cv2.VideoCapture("/Volumes/Extreme SSD/feb8_cpp_rec_11139.mp4")

# Check if the video is opened
if not video.isOpened():
    exit()

# Use this if frames need to be skipped
pos = 300
video.set(cv2.CAP_PROP_POS_FRAMES, pos)

# Get frame rate and size from input video:
frameRate = video.get(cv2.CAP_PROP_FPS)
frameSize = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Create a VideoWriter object and use size from input video
fourcc = cv2.VideoWriter_fourcc(*'H264')
outputVid = cv2.VideoWriter("output.mp4", fourcc, frameRate, frameSize)
# outputVid = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc('M','J','P','G'), frameRate, frameSize)

# Check if the video writer was successfully created
if not outputVid.isOpened():
    print("Error creating video writer")
    exit()

# Create background subtractor object
history = 2000
varThreshold = 32.0
bShadowDetection = True
bgSubtractor = cv2.createBackgroundSubtractorMOG2(history, varThreshold, bShadowDetection)

# Set history of MOG2 to decrease learning rate
# This makes the background model more stable for still animals

# Create matrix objects to store frame and background mask data
prevPoint = (0, 0)
rectangle = None
roiSelected = False
csvFile = open("centroid.csv", 'w', newline='')
csvWriter = csv.writer(csvFile)

# Loop through available frames
while True:
    ret, frame = video.read()
    if not ret:
        break

    fgndMask = bgSubtractor.apply(frame)

    # Image manipulations to compensate for noise / variance
    processed = imgProc.imgProc(fgndMask)

    # Calculate the centroid of the object being tracked
    point = centroid.centroid(processed)

    if point != (0, 0):
        prevPoint = point
    else:
        point = prevPoint

    # Add centroid to the frame
    cv2.circle(frame, (int(point[0]), int(point[1])), 5, (0, 255, 0), -1)

    # Create a rectangle object in the middle of the screen
    # rectangle = createRect.create(frame)

    # Use the following code if you would like the user to
    # Define the ROI:
    if not roiSelected:
        rectangle = cv2.selectROI(frame)
        roiSelected = True

    # Check if the point is inside rectangle
    location = pointInside.pointInside(frame, rectangle, point)

    # Add the centroid to the csv file
    csvWriter.writerow([int(point[0]), int(point[1]), location])

    # Show the frame and use waitKey to stop program
    cv2.imshow("frame", frame)

    # Write the frame to the output video
    outputVid.write(frame)

    if cv2.waitKey(25) >= 0:
        break

video.release()
outputVid.release()
cv2.destroyAllWindows()

csvFile.close()

print("Finished tracking video.")

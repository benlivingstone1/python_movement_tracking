import cv2
import pyaudio
import numpy as np
from multiprocessing import Process, Event
from scipy.io.wavfile import read, write
import time
import wave
import imgProc
import centroid
import csv
import pointInside


def play_stimuli(end_test, trigger_stim, stimuli):
    p_stim = pyaudio.PyAudio()

    # stim = wave.open('auditory_looming_stimulus.wav', 'rb')
    fs, stim = read('auditory_looming_stimulus.wav')

    # Wait for some signal to play the stimuli, play it, then stop.

    stim_stream = p_stim.open(format=pyaudio.get_format_from_width(stim.dtype.itemsize),
                         channels=len(stim.shape),
                         rate=fs,
                         output=True)


    while not end_test.is_set():
        trigger_stim.wait()

        stim_stream.write(stim.tobytes())
        trigger_stim.clear()

    stim_stream.stop_stream()
    stim_stream.close()
    p_stim.terminate()


def play_background(end_test, background):
    p = pyaudio.PyAudio()

    # bgnd = wave.open('background_noise.wav', 'r')
    chunk = 1024

    fs, bgnd = read('background_noise.wav')

    cont_stream = p.open(format=pyaudio.get_format_from_width(bgnd.dtype.itemsize),
                         channels=len(bgnd.shape),
                         rate=fs,
                         output=True)
    while not end_test.is_set():
        cont_stream.write(bgnd)

    cont_stream.stop_stream()
    cont_stream.close()
    p.terminate()


if __name__ == "__main__":
    # Create a video capture object:
    # Put a filename as argument, otherwise "0" opens default camera
    video = cv2.VideoCapture(1)

    # Check if the video is opened
    if not video.isOpened():
        exit()

    # # Use this if frames need to be skipped
    # pos = 300
    # video.set(cv2.CAP_PROP_POS_FRAMES, pos)

    # wait for a few frames
    time.sleep(0.5)

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

    '''
    Audio playback handing
    '''
    # Create events that will trigger stim and end the program
    end_test = Event()
    trigger_stim = Event()

    # Create threads to hand background and stimulus playback 
    background_process = Process(target=play_background, args=(end_test, "background_noise.wav"))
    stimulus_process = Process(target=play_stimuli, args=(end_test, trigger_stim, "auditory_looming_stimulus.wav"))

    background_process.start()
    stimulus_process.start()

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

        if location == "TRIGGER":
            trigger_stim.set()

        # Add the centroid to the csv file
        csvWriter.writerow([int(point[0]), int(point[1]), location])

        # Show the frame and use waitKey to stop program
        cv2.imshow("frame", frame)

        # Write the frame to the output video
        outputVid.write(frame)

        if cv2.waitKey(25) >= 0:
            break

    # Close windows, signal processes to clean up audio playback objects
    end_test.set()
    video.release()
    outputVid.release()
    cv2.destroyAllWindows()

    csvFile.close()

    # End the processes
    background_process.terminate()
    stimulus_process.terminate()

    print("Finished tracking video.")



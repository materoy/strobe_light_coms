import cv2
import numpy
import time
import iir_filter
from scipy import signal

# This program detects and measures the frequency of strobe lights 

capture = cv2.VideoCapture(0)

prev_frame = None

point_light_threshold = 200

time_now = time.time()

strobe_count = 0

# while not first_frame:
while True:
    # Capture video frame by frame 
    ret, frame = capture.read()

    # Unfiltered frame output
    cv2.imshow("Unfiltered output", frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # frame = cv2.GaussianBlur(frame, 2, sigmaX=5, sigmaY=5)
    frame = cv2.blur(frame, (5,5))
    min_val, max_val, min_index, max_index = cv2.minMaxLoc(frame)

    sos = signal.butter(2, [0.45], 'lowpass', analog=False, output='sos', fs=30)
    filter = iir_filter.IIR_filter(sos)
    frame = filter.filter(frame)

    if max_val > point_light_threshold:
        cv2.circle(frame, center=max_index, radius=20, color=(0, 255, 255))
        strobe_count += 1

        if time.time() - time_now >= 1:
            print(f"{strobe_count} Hz")
            time_now = time.time()
            strobe_count = 0
    
    # Display the resulting frame
    cv2.imshow('Video capture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()

cv2.destroyAllWindows()

def measure_recording_freq(capture) -> int:
    fps = capture.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    # Number of frames to capture
    num_frames = 120

    print("Capturing {0} frames".format(num_frames))

    # Start time
    start = time.time()

    # Grab a few frames
    for i in range(0, num_frames) :
        ret, frame = capture.read()

    # End time
    end = time.time()

    # Time elapsed
    seconds = end - start
    print ("Time taken : {0} seconds".format(seconds))

    # Calculate frames per second
    fps  = num_frames / seconds
    print("Estimated frames per second : {0}".format(fps))
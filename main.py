import cv2
import numpy
import time
import iir_filter
from scipy import signal
import math
import matplotlib.pylab as pl

# This program detects and measures the frequency of strobe lights 
def main():
    capture = cv2.VideoCapture(0)

    prev_frame = None

    point_light_threshold = 200

    time_now = time.time()

    strobe_count = 0

    # Sampling time in seconds
    sampling_time: int = 10
    start_sampling_time = time.time()

    sampling_freq_data = dict()

    # Collects samples for [start_sampling_time] amount of time
    while time.time() - start_sampling_time < sampling_time:
        # Capture video frame by frame 
        ret, frame = capture.read()
        
        frame_time = time.time() - time_now

        # Sampling frequency 1 / T
        sampling_frequency = int(1 / frame_time) 
        sampling_freq_data.setdefault(time.time() - start_sampling_time, sampling_frequency)
        time_now = time.time()

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

if __name__ == '__main__':
    main()
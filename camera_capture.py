import cv2

capture = cv2.VideoCapture(0)

first_frame = False

# while not first_frame:
while True:
    # Capture video frame by frame 
    first_frame, frame = capture.read()
    
    # Display the resulting frame
    cv2.imshow('Video capture', frame)
    
    fps = capture.get(cv2.CAP_PROP_FPS)
    print(fps)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# fps = capture.get(cv2.CAP_PROP_FPS)
fps = capture.get(cv2.cv.CV_CAP_PROP_FPSdd)

print(fps)
capture.release()

cv2.destroyAllWindows()
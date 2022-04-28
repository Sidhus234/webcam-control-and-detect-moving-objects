import cv2
import time
from datetime import datetime
import pandas as pd

from cv2 import threshold

# variable to store first frame (Static background)
first_frame = None

# Variables to visualize presence/absence of objects
status_list = [None, None]
times = []
df = pd.DataFrame(columns=["Start", "End"])

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()

    # variable to store if there is object in frame
    status = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur the image using Gasussian Blur
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue  # go to begining of while loop

    # Calculate difference between current frame and first frame
    delta_frame = cv2.absdiff(first_frame, gray)

    # Apply threshold to tag object
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # Smooth the threshold frame
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=3)

    # Find contours in the thresh_frame
    (cnts, _) = cv2.findContours(thresh_frame.copy(),
                                 cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Keep contours with area > 1000
    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        # Object detected
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    status_list.append(status)
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
        pass
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
        pass

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break
print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()

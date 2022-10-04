import datetime
import imutils
import time
import cv2
MIN_AREA = 1000
THRESHOLD_LEVEL = 100


vs = cv2.VideoCapture(0)
time.sleep(2)
first_frame = None
# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (500, 375))
while True:
    success, frame = vs.read()
    text = 'unocupied'
    if frame is None:
        break
    frame = imutils.resize(frame, width=500)  # change rezolution yo 500*350
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # rgb to gray
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # blair
    if first_frame is None:
        first_frame = gray
        continue
    frame_delta = cv2.absdiff(first_frame, gray)
    # cv2.imshow("Frame Delta", frame_delta)
    thresh = cv2.threshold(frame_delta, THRESHOLD_LEVEL, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("th", thresh)
    thresh_dil = cv2.dilate(thresh, None, iterations=2)
    # cv2.imshow("th2", thresh_dil)
    cnts = cv2.findContours(thresh_dil.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) < MIN_AREA:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
        text = 'occupied'
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%S %p"),
                (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow('security feed', frame)
    k = cv2.waitKey(1)  # Wait for a pressed key
    if k == ord('q'):
        break
vs.release()
cv2.destroyAllWindows()



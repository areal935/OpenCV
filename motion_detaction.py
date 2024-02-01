import datetime
import imutils
import time
import cv2
MIN_AREA = 1000
# minimal area of picsels to be considered as some big enough
THRESHOLD_LEVEL = 100
# the level that beyond and above to it the pixel will be translated to zero or 1
# therefor can be adjusted for lighting level

ROOM_OCCUPIED = 'occupied'
UN_OCCUPIED = 'NOT occupied'.upper()


vs = cv2.VideoCapture(0)
time.sleep(2)
first_frame = None
#wait for comera to be reddy

#TODO fix writing to file
# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (500, 375))
while True:
    success, frame = vs.read()
    text = UN_OCCUPIED
    # massage if there is smale difference with the basic frame

    # if comera shout down suddenly exit the loop
    if frame is None:
        break

    frame = imutils.resize(frame, width=500)  # change rezolution yo 500*350q
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # rgb to gray
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # blair convolution with gausian

    # if frame being not redy
    if first_frame is None:
        first_frame = gray
        continue

    # delta with base frame
    frame_delta = cv2.absdiff(first_frame, gray)
    # cv2.imshow("Frame Delta", frame_delta)

    # binary picture
    thresh = cv2.threshold(frame_delta, THRESHOLD_LEVEL, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("th", thresh)

    # spreading frame twice
    thresh_dil = cv2.dilate(thresh, None, iterations=2)
    # cv2.imshow("th2", thresh_dil)

    # marking the areas that has been changed
    cnts = cv2.findContours(thresh_dil.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:

        # area to small
        if cv2.contourArea(c) < MIN_AREA:
            continue

        # building the triangle around the areas
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

        text = ROOM_OCCUPIED
        #chenge room status

    # write the date and
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%S %p"),
                (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow('security feed', frame)

    # exit when 'q' is presed
    k = cv2.waitKey(1)  # Wait for a pressed key
    if k == ord('q'):
        break

#close properly
vs.release()
cv2.destroyAllWindows()
 
import datetime
import imutils
import time
import cv2
import numpy as np
MIN_COL_DIFF = 20
TOTAL_DIFF = 100000
MIN_SEC = 10
MAX_FRAME_NAM = 100


def list_to_range(list1):
    list2 = []
    start = list1[0]
    for num in list1:
        end = num
        if num - 1 not in list1:
            start = num
        if num + 1 not in list1:
            list2.append((start, end))
    return list2

stuck_frames = []

vs = cv2.VideoCapture('VideoGame.mp4')
num_of_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(vs.get(cv2.CAP_PROP_FPS))
width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
# print(num_of_frames, height, width)
# while vs.isOpened():
# p_frame = np.zeros((width, height))
success, p_frame = vs.read()
p_frame = cv2.cvtColor(p_frame, cv2.COLOR_BGR2GRAY)  # rgb to gray
stack_flug = False
for i in range(1, num_of_frames):
    success, frame = vs.read()
    k = cv2.waitKey(1)  # Wait for a pressed key
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # rgb to gray
    # np_frame
    frame_delta = cv2.absdiff(p_frame, gray)
    map(lambda x: 0 if x < MIN_COL_DIFF else x, frame_delta)
    total_diff = np.sum(frame_delta)
    if total_diff < TOTAL_DIFF:
        # print(total_diff, i)
        stuck_frames.append(i)
        # cv2.imshow('prev', p_frame)
        # cv2.waitKey(0)
    p_frame = gray

    cv2.imshow('video', gray)

    k = cv2.waitKey(1)  # Wait for a pressed key
    if k == ord('q'):
        break
print(f'total: {len(stuck_frames)},: {stuck_frames}')
print(list_to_range(stuck_frames))
print(len(list_to_range(stuck_frames)))
vs.release()
cv2.destroyAllWindows()

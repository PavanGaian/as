import cv2
import numpy as np


trackers = {
    #'csrt': cv2.TrackerCSRT_create,
    #'mosse': cv2.TrackerMOSSE_create,
    'mil' : cv2.TrackerMIL_create,
    #'kcf' : cv2.TrackerKCF_create,
    #'medianflow' : cv2.TrackerMedianFlow_create,
}

tracker_key = 'mil'
roi = None
tracker = trackers[tracker_key]()

cap = cv2.VideoCapture(0)
count = 0
prev_state = None

while True:
    frame = cap.read()[1]

    if frame is None:
        break
    
    frame = cv2.resize(frame, (750, 550))
    
    if roi is not None:
        success, box = tracker.update(frame)
        
        if success:
            x, y, w, h = [int(c) for c in box]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            if box != prev_state:
                print("Moving box", count)
                count += 1
                prev_state = box
        else:
            print("Tracking failed")
            roi = None
            tracker = trackers[tracker_key]()

        frame_height, frame_width, _ = frame.shape
        
        if w > 5 and h > 5 and box not in (x, y, w, h):
            print("Bounding box:", (x, y, w, h))

            #if x<=0 or y<=0 :
        
            if x <= 0  or y <= 0 or x + w > frame_width or y + h > frame_height:
                print("Object removed")
                roi = cap
                

        

    cv2.imshow('Tracking', frame)
    k = cv2.waitKey(30)

    if k == ord('s'):
        roi = cv2.selectROI('Tracking', frame)
        tracker.init(frame, roi)
        
    elif k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

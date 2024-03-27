import cv2
import numpy as np

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Initialize tracker
trackers = {
    'mil': cv2.TrackerMIL_create,
}
tracker_key = 'mil'
roi = None
tracker = trackers[tracker_key]()

# Open video capture
cap = cv2.VideoCapture(0)

box = None

while True:
    # Read frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame
    frame = cv2.resize(frame, (750, 550))

    # Object tracking
    if roi is not None:
        success, box = tracker.update(frame)
        if success:
            x, y, w, h = [int(c) for c in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        else:
            print("Tracking failed")
            roi = None

    # Object detection
    frame_height, frame_width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                w = int(detection[2] * frame_width)
                h = int(detection[3] * frame_height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                if w > 5 and h > 5:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), colors[class_id], 2)
                    if box != (x, y, w, h):
                        print("Bounding box:", (x, y, w, h))
                        if x <= 0 or y <= 0 or x + w > frame_width or y + h > frame_height:
                            print("Object removed")
                            roi = None

    # Show frame
    cv2.imshow('Tracking', frame)

    # Check for key press
    key = cv2.waitKey(1)
    if key == ord('s'):
        roi = cv2.selectROI('Tracking', frame)
        tracker.init(frame, roi)
    elif key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

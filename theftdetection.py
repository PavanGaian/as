import cv2
import numpy as np
import requests


def detecting():

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
    cap = cv2.VideoCapture('test.mp4')#("rtsp://gaian1234:gaian1234@192.168.0.192/stream1")#(0)#(rtsp://camerausername:camerapassword@camerawifiip/stream1(or)stream2)

    box = None
    url = "https://ig.gaiansolutions.com/mobius-content-service/v1.0/content/upload?override=true&filePath=%2Fbottle%2Flimka%2Fsoda%2F&filePathAccess=private"

    payload={}
    files=[]
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZmOGYxNjhmLTNmZjYtNDZlMi1iMTJlLWE2YTdlN2Y2YTY5MCJ9.eyJwcm9maWxlVXJsIjoid3d3Lmdvb2dsZS5jb20vaW1hZ2VzL2F2aW5hc2gtcGF0ZWwtcm9ja3oiLCJyZWNlbnRfc2Vzc2lvbiI6Ik5BIiwic3ViIjoiZ2FpYW4uY29tIiwicGFyZW50VGVuYW50SWQiOiJOQSIsImNvbG9yIjpudWxsLCJ1c2VyX25hbWUiOiJtb2JpbGUxMEBnYXRlc3RhdXRvbWF0aW9uLmNvbSIsImlzcyI6ImdhaWFuLmNvbSIsImlzQWRtaW4iOnRydWUsInBsYXRmb3JtSWQiOiI2NWNmMGU1MWMzNGZmYjA3ZDg1NTQ4YWUiLCJ1c2VyTmFtZSI6Im1vYmlsZTEwQGdhdGVzdGF1dG9tYXRpb24uY29tIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9NQVJLRVRQTEFDRV9VU0VSIl0sImNsaWVudF9pZCI6ImdhaWFuIiwic2NvcGUiOlsidHJ1c3QiLCJyZWFkIiwid3JpdGUiXSwidGVuYW50SWQiOiI2NWNmMGJkNzlkNTU0MjAwMDFhYTdjMjIiLCJsb2dvIjoid3d3Lmdvb2dsZS5jb20vaW1hZ2VzLiIsImV4cCI6MTcwODExMjEyMiwianRpIjoiYzM1NDdlYjUtMGY3Yi00YWMyLTg4ZDgtMTI1YzY0ZDcxOTgzIiwiZW1haWwiOiJtaWFzdGVzdGVudkBnYXRlc3RhdXRvbWF0aW9uLmNvbSJ9.i-I_6i_I6r8_fWAf0d-uZEZxxcFfcOjheYApaN9PRZx7OhFd0mw-GTlbjRgVyQK2Nm5cVfNt6KdXM7elm3rS1MPJOPZqr5n6fmh7Jg1vo8i4b0gyNT5N3XxVNMUQATK2sZsPZFOS1p6hZzE2kZ4mtvuXgxGtHpbSNhzgf7iShBFFGD-pUBQ3DRYM5BkbkORpgzyizgA0Qd0LOiLMJKrasjnGtNUfDcHHTd6YTfkSIA649YNDh5sWKl2CbD5UkIJie7m8roLl3Ipuu4At8Y5qlgh14XaU5jXrCV-Uy7Ze8TQyWEqYD07RQZb0E3KrndjQojG8WS3IM5yBOLAI3fsWMQeyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZmOGYxNjhmLTNmZjYtNDZlMi1iMTJlLWE2YTdlN2Y2YTY5MCJ9.eyJwcm9maWxlVXJsIjoid3d3Lmdvb2dsZS5jb20vaW1hZ2VzL2F2aW5hc2gtcGF0ZWwtcm9ja3oiLCJyZWNlbnRfc2Vzc2lvbiI6Ik5BIiwic3ViIjoiZ2FpYW4uY29tIiwicGFyZW50VGVuYW50SWQiOiJOQSIsImNvbG9yIjpudWxsLCJ1c2VyX25hbWUiOiJtb2JpbGUxMEBnYXRlc3RhdXRvbWF0aW9uLmNvbSIsImlzcyI6ImdhaWFuLmNvbSIsImlzQWRtaW4iOnRydWUsInBsYXRmb3JtSWQiOiI2NWNmMGU1MWMzNGZmYjA3ZDg1NTQ4YWUiLCJ1c2VyTmFtZSI6Im1vYmlsZTEwQGdhdGVzdGF1dG9tYXRpb24uY29tIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9NQVJLRVRQTEFDRV9VU0VSIl0sImNsaWVudF9pZCI6ImdhaWFuIiwic2NvcGUiOlsidHJ1c3QiLCJyZWFkIiwid3JpdGUiXSwidGVuYW50SWQiOiI2NWNmMGJkNzlkNTU0MjAwMDFhYTdjMjIiLCJsb2dvIjoid3d3Lmdvb2dsZS5jb20vaW1hZ2VzLiIsImV4cCI6MTcwODExMjEyMiwianRpIjoiYzM1NDdlYjUtMGY3Yi00YWMyLTg4ZDgtMTI1YzY0ZDcxOTgzIiwiZW1haWwiOiJtaWFzdGVzdGVudkBnYXRlc3RhdXRvbWF0aW9uLmNvbSJ9.i-I_6i_I6r8_fWAf0d-uZEZxxcFfcOjheYApaN9PRZx7OhFd0mw-GTlbjRgVyQK2Nm5cVfNt6KdXM7elm3rS1MPJOPZqr5n6fmh7Jg1vo8i4b0gyNT5N3XxVNMUQATK2sZsPZFOS1p6hZzE2kZ4mtvuXgxGtHpbSNhzgf7iShBFFGD-pUBQ3DRYM5BkbkORpgzyizgA0Qd0LOiLMJKrasjnGtNUfDcHHTd6YTfkSIA649YNDh5sWKl2CbD5UkIJie7m8roLl3Ipuu4At8Y5qlgh14XaU5jXrCV-Uy7Ze8TQyWEqYD07RQZb0E3KrndjQojG8WS3IM5yBOLAI3fsWMQ'
    }
    #data = {
    #    "theftdetected":"Yes"
    #}
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
                                cv2.imwrite('object_removed_screenshot.jpg', frame)
                                # call test file
                                #response = requests.request("POST", url, headers=headers, data=payload, files=files)
                                #requests.post(url, headers=headers, data=payload, files=files)
                                try:
                                    files = {'image': open('object_removed_screenshot.jpg', 'rb')}
                                    response = requests.post(url, headers=headers, files=files)
                                    if response.status_code == 200:
                                        print("Image successfully sent.")
                                    else:
                                        print("Error:", response.status_code)
                                except Exception as e:
                                    print("Error sending image:", e)

                                roi = None
                                #if 'object_removed_screenshot.jpg' in files:
                                 #   response = requests.request("POST", url,  headers=headers, data=payload, files=files)

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



detecting()
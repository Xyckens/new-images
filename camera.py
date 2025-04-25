import cv2
import time
import os

# Set up camera (for Jetson Nano CSI camera, use the GStreamer pipeline)
def gstreamer_pipeline(
        capture_width=1280,
        capture_height=720,
        display_width=1280,
        display_height=720,
        framerate=30,
        flip_method=0,
):
    return (
        f"nvarguscamerasrc ! video/x-raw(memory:NVMM), "
        f"width=(int){capture_width}, height=(int){capture_height}, "
        f"format=(string)NV12, framerate=(fraction){framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width=(int){display_width}, height=(int){display_height}, "
        f"format=(string)BGRx ! videoconvert ! "
        f"video/x-raw, format=(string)BGR ! appsink"
    )

# Choose source: for CSI camera use gstreamer_pipeline(), for USB use cv2.VideoCapture(0)
cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
# cap = cv2.VideoCapture(0)  # Uncomment for USB webcam

if not cap.isOpened():
    print("Camera could not be opened.")
    exit()

frame_count = 0
saved_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        frame_count += 1

        if frame_count % 60 == 0:
            filename = f"frame_{saved_count:04d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")
            saved_count += 1

        # Optional: show live preview
        # cv2.imshow('Camera', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
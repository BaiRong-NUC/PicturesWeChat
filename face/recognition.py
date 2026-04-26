import face_recognition
import cv2
from feature_extraction import FeatureExtractor


WINDOW_NAME = "Video"

user_features = FeatureExtractor("./data").user_features
print("Extracted user features:", user_features)


# def is_window_closed(window_name):
#     try:
#         return cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1
#     except cv2.error:
#         return True


# video_capture = cv2.VideoCapture(0)

# while True:
#     ret, frame = video_capture.read()
#     if not ret:
#         break

#     face_locations = face_recognition.face_locations(frame)

#     for top, right, bottom, left in face_locations:
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#     cv2.imshow(WINDOW_NAME, frame)

#     key = cv2.waitKey(1) & 0xFF
#     if key == ord("q") or is_window_closed(WINDOW_NAME):
#         break

# video_capture.release()
# cv2.destroyAllWindows()

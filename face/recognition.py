import face_recognition
import cv2
from .feature_extraction import FeatureExtractor


class FaceRecognition:
    def __init__(self, dataset_dir, video_source=0, window_name="Video"):
        self.window_name = window_name
        self.user_features = FeatureExtractor(dataset_dir).user_features
        self.video_capture = cv2.VideoCapture(video_source)

    def close(self) -> bool:
        if self.video_capture is not None and self.video_capture.isOpened():
            self.video_capture.release()

        try:
            if not self.is_window_closed():
                cv2.destroyWindow(self.window_name)
            cv2.waitKey(1)  # 等待窗口关闭事件，确保窗口被销毁
        except (AttributeError, cv2.error):
            print("window already closed or does not exist.")
            pass

        return True

    def is_window_closed(self) -> bool:
        try:
            return cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1
        except cv2.error:
            return True

    def loop_recognization(self) -> bool:
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            face_locations = face_recognition.face_locations(frame)

            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.imshow(self.window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or self.is_window_closed():
                break
        return self.close()


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

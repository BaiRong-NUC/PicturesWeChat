import face_recognition
import cv2
from .feature_extraction import FeatureExtractor
from wechat.user import User
import time
import threading


class FaceRecognition:
    def __init__(
        self,
        dataset_dir,
        video_source=0,
        window_name="Video",
        frame_scale=0.5,
        process_every_n_frames=3,
        recognition_tolerance=0.6,
        unknown_alert_interval=60,
    ):
        self.window_name = window_name
        self.user_features = FeatureExtractor(dataset_dir).user_features
        self.known_user_names = list(self.user_features.keys())
        self.known_user_features = list(self.user_features.values())
        self.video_capture = cv2.VideoCapture(video_source)
        self.frame_scale = frame_scale
        self.process_every_n_frames = max(1, process_every_n_frames)
        self.recognition_tolerance = recognition_tolerance
        self.unknown_alert_interval = unknown_alert_interval
        self.frame_index = 0
        self.last_recognition_results = []
        self.last_unknown_alert_time = 0
        self.is_sending_unknown_alert = False

        # 用户
        self.user = User(refresh_token=False)

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

    def draw_recognition_result(self, frame, face_location, user_name=None):
        top, right, bottom, left = face_location
        if user_name:
            label = f"{user_name}"
            color = (0, 255, 0)  # 绿色表示识别成功
        else:
            label = "Unknown"
            color = (0, 0, 255)  # 红色表示未识别

        # 绘制人脸边界框
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # 绘制标签背景
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        label_top = max(top - label_size[1], 0)
        cv2.rectangle(
            frame,
            (left, label_top),
            (left + label_size[0], label_top + label_size[1]),
            color,
            cv2.FILLED,
        )

        # 绘制标签文本
        cv2.putText(
            frame,
            label,
            (left, label_top + label_size[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

    def notify_unknown_person(self, unknown_count=1):
        now = time.monotonic()
        if now - self.last_unknown_alert_time < self.unknown_alert_interval:
            return
        if self.is_sending_unknown_alert:
            return

        self.last_unknown_alert_time = now
        detected_time = time.strftime("%Y-%m-%d %H:%M:%S")
        message = f"Unknown person detected at {detected_time}"
        if unknown_count > 1:
            message = f"{unknown_count} unknown people detected at {detected_time}"

        def send_alert():
            self.is_sending_unknown_alert = True
            try:
                self.user.send_message(message)
            finally:
                self.is_sending_unknown_alert = False

        threading.Thread(target=send_alert, daemon=True).start()

    @staticmethod
    def scale_face_location(face_location, scale):
        top, right, bottom, left = face_location
        return (
            int(top * scale),
            int(right * scale),
            int(bottom * scale),
            int(left * scale),
        )

    def match_user(self, face_encoding):
        if not self.known_user_features:
            return None

        matches = face_recognition.compare_faces(
            self.known_user_features,
            face_encoding,
            tolerance=self.recognition_tolerance,
        )
        if not any(matches):
            return None

        face_distances = face_recognition.face_distance(
            self.known_user_features,
            face_encoding,
        )
        best_match_index = face_distances.argmin()
        if matches[best_match_index]:
            return self.known_user_names[best_match_index]

        return None

    def recognize_frame(self, frame):
        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=self.frame_scale,
            fy=self.frame_scale,
        )
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        small_face_locations = face_recognition.face_locations(rgb_frame, model="hog")

        # 提取当前帧中检测到的人脸特征,与用户特征进行比较
        face_encodings = face_recognition.face_encodings(
            rgb_frame,
            small_face_locations,
        )
        location_scale = 1 / self.frame_scale
        recognition_results = []

        for small_face_location, face_encoding in zip(
            small_face_locations,
            face_encodings,
        ):
            face_location = self.scale_face_location(
                small_face_location, location_scale
            )
            recognized_user = self.match_user(face_encoding)
            recognition_results.append((face_location, recognized_user))

        return recognition_results

    def loop_recognization(self) -> bool:
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            if self.frame_index % self.process_every_n_frames == 0:
                self.last_recognition_results = self.recognize_frame(frame)
                unknown_count = sum(
                    1
                    for _, recognized_user in self.last_recognition_results
                    if recognized_user is None
                )
                if unknown_count > 0:
                    self.notify_unknown_person(unknown_count)
            self.frame_index += 1

            for face_location, recognized_user in self.last_recognition_results:
                # 显示识别结果
                self.draw_recognition_result(frame, face_location, recognized_user)

            cv2.imshow(self.window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or self.is_window_closed():
                break
        return self.close()

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

    def loop_recognization(self) -> bool:
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)

            # 提取当前帧中检测到的人脸特征,与用户特征进行比较
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_location, face_encoding in zip(face_locations, face_encodings):
                recognized_user = None
                for user_name, user_feature in self.user_features.items():
                    matches = face_recognition.compare_faces(
                        [user_feature], face_encoding
                    )
                    if matches[0]:
                        recognized_user = user_name
                        break
                # 显示识别结果
                self.draw_recognition_result(frame, face_location, recognized_user)

            cv2.imshow(self.window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or self.is_window_closed():
                break
        return self.close()

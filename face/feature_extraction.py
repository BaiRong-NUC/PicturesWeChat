# 从数据集中提取用户特征

from pathlib import Path

import numpy as np
import face_recognition


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


class FeatureExtractor:
    def __init__(self, dataset_dir):
        self.dataset_dir = Path(dataset_dir)
        self.user_features = {}  # 存储用户特征的字典
        self.extract_features()

    def extract_features(self):
        self.user_features.clear()

        for image_path in sorted(self.dataset_dir.iterdir()):
            if not image_path.is_file():
                continue
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            user_name = image_path.stem
            image = face_recognition.load_image_file(str(image_path))
            face_locations = face_recognition.face_locations(image)
            if not face_locations:
                print(f"unrecognized face skiped! picture: {image_path.name}")
                continue

            # 如果检测到多张人脸，选择最大的那一张
            face_location = self.get_largest_face_location(face_locations)
            face_encoding = face_recognition.face_encodings(image, [face_location])[0]
            self.user_features[user_name] = np.array(face_encoding)

        return self.user_features

    # 获取最大的脸部位置
    @staticmethod
    def get_largest_face_location(face_locations):
        return max(
            face_locations,
            key=lambda location: (location[2] - location[0])
            * (location[1] - location[3]),
        )

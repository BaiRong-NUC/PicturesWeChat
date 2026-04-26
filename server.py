from wechat.user import User
from face.recognition import FaceRecognition

if __name__ == "__main__":
    user = User(refresh_token=False)
    user.send_message("Hello, this is a test message from the server!")
    # print("Server is running...")
    # face_recognition = FaceRecognition(
    #     dataset_dir="./data", frame_scale=0.75, process_every_n_frames=10
    # )

    # bool_result = face_recognition.loop_recognization()
    # print(f"Face recognition loop ended with result: {bool_result}")

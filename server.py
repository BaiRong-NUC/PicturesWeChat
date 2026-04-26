from pathlib import Path

from face.recognition import FaceRecognition
from web.app import start_in_thread
from web.event_store import StrangerEventStore

WWWROOT_DIR = Path(__file__).parent / "wwwroot"
SNAPSHOT_DIR = WWWROOT_DIR / "snapshots"
EVENTS_FILE = Path(__file__).parent / "store" / "events.json"


if __name__ == "__main__":
    print("Server is running...")

    event_store = StrangerEventStore(storage_file=EVENTS_FILE)
    start_in_thread(event_store, wwwroot_dir=WWWROOT_DIR, host="0.0.0.0", port=8000)

    face_recognition = FaceRecognition(
        dataset_dir="./data",
        frame_scale=0.75,
        process_every_n_frames=10,
        event_store=event_store,
        snapshot_dir=SNAPSHOT_DIR,
        snapshot_url_prefix="snapshots",
    )

    bool_result = face_recognition.loop_recognization()
    print(f"Face recognition loop ended with result: {bool_result}")

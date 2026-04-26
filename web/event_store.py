import json
import threading
import uuid
from pathlib import Path


class StrangerEventStore:
    """线程安全的陌生人事件存储，事件持久化为 JSON 文件。"""

    def __init__(self, storage_file, max_events=500):
        self.storage_file = Path(storage_file)
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.max_events = max_events
        self._lock = threading.Lock()
        self._events = self._load()

    def _load(self):
        if not self.storage_file.exists():
            return []
        try:
            with self.storage_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
        return []

    def _save_unlocked(self):
        tmp_file = self.storage_file.with_suffix(self.storage_file.suffix + ".tmp")
        with tmp_file.open("w", encoding="utf-8") as f:
            json.dump(self._events, f, ensure_ascii=False, indent=2)
        tmp_file.replace(self.storage_file)

    def add_event(self, timestamp, unknown_count, image_path):
        event = {
            "id": uuid.uuid4().hex,
            "timestamp": timestamp,
            "unknown_count": unknown_count,
            "image": image_path,
        }
        with self._lock:
            self._events.append(event)
            if len(self._events) > self.max_events:
                self._events = self._events[-self.max_events :]
            self._save_unlocked()
        return event

    def list_events(self):
        with self._lock:
            return list(reversed(self._events))

    def clear(self):
        with self._lock:
            self._events = []
            self._save_unlocked()

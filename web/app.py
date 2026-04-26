import threading
from pathlib import Path

from flask import Flask, jsonify, send_from_directory


def create_app(event_store, wwwroot_dir):
    wwwroot_path = Path(wwwroot_dir).resolve()
    app = Flask(__name__, static_folder=None)

    @app.route("/")
    def index():
        return send_from_directory(str(wwwroot_path), "index.html")

    @app.route("/api/events")
    def list_events():
        return jsonify({"events": event_store.list_events()})

    @app.route("/api/events/clear", methods=["POST"])
    def clear_events():
        event_store.clear()
        return jsonify({"ok": True})

    @app.route("/<path:filename>")
    def static_files(filename):
        return send_from_directory(str(wwwroot_path), filename)

    return app


def start_in_thread(event_store, wwwroot_dir, host="0.0.0.0", port=8000):
    app = create_app(event_store, wwwroot_dir)

    def _run():
        app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)

    thread = threading.Thread(target=_run, name="web-server", daemon=True)
    thread.start()
    print(f"Web server started at http://{host}:{port}")
    return thread

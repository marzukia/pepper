from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from queue import Queue
import time
import threading


class SourceFileHandler(FileSystemEventHandler):
    def __init__(self, pattern: str = None):
        self.pattern = pattern or (".md", ".css", ".js")
        self.event_q = Queue()
        self.dummy_thread = None

    def on_any_event(self, event):
        print(event)
        if not event.is_directory and event.src_path.endswith(self.pattern):
            self.event_q.put((event, time.time()))

    def start(self):
        self.dummy_thread = threading.Thread(target=self._process)
        self.dummy_thread.daemon = True
        self.dummy_thread.start()

    def _process(self):
        while True:
            time.sleep(1)


handler = SourceFileHandler()
handler.start()


def run_watcher():
    observer = Observer()
    observer.schedule(handler, "example/", recursive=True)
    observer.start()
    try:
        while True:
            while not handler.event_q.empty():
                event, ts = handler.event_q.get()
                print(event.src_path)
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

"""Terminal loader animation shown while the model / tools are thinking.

Usage (sync code - planner, format_answer):

    from loader import thinking

    with thinking("Planning..."):
        response = client.chat.completions.create(...)

Usage (async code):

    with thinking("Running tool..."):
        result = await execute_action(...)

Works via a background thread, so it keeps spinning even while
the main thread is blocked on a sync OpenAI HTTP call.
"""

import sys
import threading
import time


_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


class ThinkingLoader:
    def __init__(self, message="Thinking...", interval=0.08):
        self.message = message
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1)
            self._thread = None
        # Clear the spinner line.
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()

    def _spin(self):
        i = 0
        while not self._stop_event.is_set():
            frame = _FRAMES[i % len(_FRAMES)]
            sys.stdout.write(f"\r{frame} {self.message}")
            sys.stdout.flush()
            i += 1
            # wait() so we stop immediately instead of sleeping through
            self._stop_event.wait(self.interval)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False


def thinking(message="Thinking..."):
    """Create a loader context manager: `with thinking('...'): ...`"""
    return ThinkingLoader(message)

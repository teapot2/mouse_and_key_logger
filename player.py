from pynput import mouse, keyboard
import datetime
import json
import time
from enum import Enum


class EventType(Enum):
    MOUSE_MOVE = "mouse_move"
    MOUSE_CLICK = "mouse_click"
    MOUSE_RELEASE = "mouse_release"
    MOUSE_SCROLL = "mouse_scroll"
    KEY_PRESS = "key_press"
    KEY_RELEASE = "key_release"


class Player:
    def __init__(self, file_path):
        """Initialize the Player with the file path of the recorded data."""
        self.file_path = file_path
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

    def load_data(self):
        """Load the recorded data from the file."""
        with open(self.file_path, "r") as file:
            self.recorded_data = json.load(file)

    def play(self):
        """Play back the recorded mouse and keyboard movements."""
        start_time = self._get_time(self.recorded_data[0])

        for data in self.recorded_data:
            event_time = self._get_time(data)
            delay = (event_time - start_time).total_seconds()
            time.sleep(delay)

            if data["event_type"] == EventType.MOUSE_MOVE.value:
                self._handle_mouse_move(data)
            elif data["event_type"] in [
                EventType.MOUSE_CLICK.value,
                EventType.MOUSE_RELEASE.value,
            ]:
                self._handle_mouse_click_or_release(data)
            elif data["event_type"] == EventType.MOUSE_SCROLL.value:
                self._handle_mouse_scroll(data)
            elif data["event_type"] in [
                EventType.KEY_PRESS.value,
                EventType.KEY_RELEASE.value,
            ]:
                self._handle_key_press_or_release(data)

            start_time = event_time

    def _get_time(self, data):
        """Extract the timestamp from the data and convert it to a datetime object."""
        return datetime.datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S.%f")

    def _handle_mouse_move(self, data):
        """Handle a mouse move event."""
        self.mouse_controller.position = data["position"]

    def _handle_mouse_click_or_release(self, data):
        """Handle a mouse click or release event."""
        button = getattr(mouse.Button, data["button"])
        if data["event_type"] == EventType.MOUSE_CLICK.value:
            self.mouse_controller.press(button)
        else:
            self.mouse_controller.release(button)

    def _handle_mouse_scroll(self, data):
        """Handle a mouse scroll event."""
        self.mouse_controller.scroll(*data["scroll_direction"])

    def _handle_key_press_or_release(self, data):
        """Handle a key press or release event."""
        key = data["key"]
        if key.startswith("Key."):
            key = getattr(keyboard.Key, key[4:])
        if data["event_type"] == EventType.KEY_PRESS.value:
            self.keyboard_controller.press(key)
        else:
            self.keyboard_controller.release(key)

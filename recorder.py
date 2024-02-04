import os
import time
import datetime
import pyautogui
import threading
import logging
import json
from pynput import mouse, keyboard


# SLEEP_INTERVAL: The interval in seconds to sleep between iterations
SLEEP_INTERVAL = 0.1


class Recorder:
    def __init__(self, session_id):
        self.session_id = session_id
        self.recorded_data = []
        self.stop_listeners = threading.Event()

    def on_move(self, x, y):
        """Handle mouse movement event."""
        self.record_event("mouse_move", position=(x, y))
        logging.info(f"Mouse moved to position: {x}, {y}")

    def on_click(self, x, y, button, pressed):
        """Handle mouse click event."""
        event_type = "mouse_click" if pressed else "mouse_release"
        self.record_event(event_type, position=(x, y), button=button.name)
        logging.info(f"Mouse {event_type}: {button.name} clicked at position: {x}, {y}")

    def on_scroll(self, x, y, dx, dy):
        """Handle mouse scroll event."""
        self.record_event("mouse_scroll", position=(x, y), scroll_direction=(dx, dy))
        logging.info(
            f"Mouse scrolled at position: {x}, {y}, scroll direction: {dx}, {dy}"
        )

    def on_press(self, key):
        """Handle key press event."""
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key)
        self.record_event("key_press", key=key_name)
        logging.info(f"Key pressed: {key_name}")

    def on_release(self, key):
        """Handle key release event."""
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key)
        self.record_event("key_release", key=key_name)
        logging.info(f"Key released: {key_name}")
        if key == keyboard.Key.esc:
            # Stop recording if the Escape key is pressed
            self.stop_listeners.set()
            logging.info("Escape key pressed, stopping listeners.")
            return False

    def record_event(self, event_type, **kwargs):
        """Record an event with the given type and attributes."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        data = {"timestamp": timestamp, "event_type": event_type, **kwargs}
        self.recorded_data.append(data)

    def take_screenshot_periodically(self, time_to_wait_in_seconds):
        """Take a screenshot every SCREENSHOT_INTERVAL seconds."""
        screenshots_folder = os.path.join(os.path.dirname(__file__), "screenshots")
        session_folder = os.path.join(
            screenshots_folder,
            datetime.datetime.now().strftime("%Y%m%d") + "_" + self.session_id,
        )

        os.makedirs(session_folder, exist_ok=True)

        while not self.stop_listeners.is_set():
            time.sleep(time_to_wait_in_seconds)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            filename = f"_{timestamp}_{self.session_id}.png"

            pyautogui.screenshot(os.path.join(session_folder, filename))

            logging.info(
                f"Screenshot taken at {timestamp} and saved as {filename} in {session_folder}"
            )

    def start(self, screenshot_interval):
        """Start recording mouse and keyboard movements."""
        # Initialize mouse and keyboard listeners
        mouse_listener = mouse.Listener(
            on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
        )
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )

        # Start threads for mouse and keyboard listeners
        mouse_thread = threading.Thread(target=mouse_listener.start)
        keyboard_thread = threading.Thread(target=keyboard_listener.start)

        # Start thread for taking screenshots periodically
        screenshot_thread = threading.Thread(
            target=self.take_screenshot_periodically, args=(screenshot_interval,)
        )

        mouse_thread.start()
        keyboard_thread.start()
        screenshot_thread.start()

        # Keep the threads running until stop signal is set
        while not self.stop_listeners.is_set():
            time.sleep(SLEEP_INTERVAL)

    def save(self, file_path):
        """Save the recorded data to a file."""
        try:
            with open(file_path, "w") as file:
                json.dump(self.recorded_data, file)
        except Exception as e:
            logging.error(f"Failed to save recorded data: {e}")

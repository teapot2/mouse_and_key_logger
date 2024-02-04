import argparse
import uuid
import os
from recorder import Recorder
from player import Player

# The interval in seconds to take a screenshot
SCREENSHOT_INTERVAL = 2


def main(mode, screenshot_interval):
    """Main function to record mouse and keyboard movements."""
    session_id = str(uuid.uuid4())
    file_path = os.path.join(os.path.dirname(__file__), "recorded_data.json")

    if mode == "record":
        recorder = Recorder(session_id)
        recorder.start(screenshot_interval)
        recorder.save(file_path)
    elif mode == "play":
        player = Player(file_path)
        player.load_data()
        player.play()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Record or play back mouse and keyboard movements and save screenshots."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["record", "play"],
        default="record",
        help='Mode to run the script in. "record" to record movements, "play" to play them back. (Default: %(default)s)',
    )
    parser.add_argument(
        "--ss-interval",
        type=int,
        default=SCREENSHOT_INTERVAL,
        help="Interval in seconds for taking screenshots when in record mode. (Default: %(default)s)",
    )
    args = parser.parse_args()

    main(args.mode, args.ss_interval)

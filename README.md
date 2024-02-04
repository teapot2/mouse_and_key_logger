# Mouse and Keyboard Recorder/Player

This Python script allows users to record and play back mouse and keyboard movements while capturing screenshots at specified intervals.

*For educational purposes only.*

## Features
- Record mouse and keyboard movements.
- Play back recorded sessions.
- Capture screenshots at defined intervals during the recording process.
- Utilizes a simple command-line interface.

## Getting Started

### Prerequisites
- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
  - [keyboard](https://github.com/boppreh/keyboard)
  - [Pillow](https://pillow.readthedocs.io/en/stable/)

### Installation
1. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

#### Record Mode
To record mouse and keyboard movements with screenshot capture, run the following command:

```bash
python main.py --mode record --ss-interval 2
```
- **--mode:** Set to "record" to enter record mode.
- **--ss-interval:** Set the screenshot capture interval in seconds (default is 2 seconds).

Recorded data will be saved in a file named **recorded_data.json** in the script's directory.

#### Play Mode
To play back a recorded session, use the following command:
```bash
python main.py --mode play
```
- **--mode**: Set to "play" to enter play mode.
  The script will load the recorded data from **recorded_data.json** and replay the mouse and keyboard movements.

### Contributing
Contributions are welcome! Feel free to open issues or pull requests.

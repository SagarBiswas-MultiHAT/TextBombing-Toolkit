# Message Boombing (safe, improved)

<div align="right">

[![CI](https://github.com/SagarBiswas-MultiHAT/TextBombing-Toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/SagarBiswas-MultiHAT/TextBombing-Toolkit/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

>A small, interactive Python utility for sending repeated messages using your keyboard. This project is intentionally conservative and includes safety features so you can use it responsibly.

## Project summary

This repository contains two improved variants of a simple "message bomber" utility that uses PyAutoGUI to send a message repeatedly to whichever input field is focused. The primary goals are:

- Usability: easy interactive prompts and optional CLI arguments.
- Safety: built-in failsafe, confirmation prompts, dry-run mode.
- Portability: works on common desktop OSes (Windows, macOS, Linux) where PyAutoGUI is supported.

Files of interest
- `messageBoombingV2.py` — the recommended, improved entrypoint (interactive + CLI).
- `message boombing-v1.py` — the original script (kept for reference).

Important: When using either script, the program will send keystrokes to whatever window is focused. Move your mouse to the top-left corner to trigger PyAutoGUI's failsafe and abort sending immediately.

## Features (what's new / improved)

- Interactive and CLI modes (use `-m` / `--message`, `-c` / `--count`, etc.)
- Dry-run mode (`--dry-run`) — prints what would be sent without sending it
- Clipboard paste option (`--clipboard`) for large messages (uses `pyperclip`)
- Confirm prompt and a 5-second countdown before sending
- PyAutoGUI failsafe enabled — move mouse to top-left corner to abort
- Robust input validation and clear error messages

## Quick start

Prerequisites

- Python 3.8+ (3.11 recommended)
- Optional: `pyperclip` for clipboard paste functionality
- Optional: `pyautogui` to actually send keystrokes (required to run non-dry-run)

Install (recommended in a virtual environment)

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate      # Windows PowerShell
python -m pip install -r requirements.txt
```

Run (interactive)

```bash
python messageBoombingV2.py
```

Run with command-line args

```bash
# Dry-run (safe): will only print what would be sent
python messageBoombingV2.py --dry-run -m "Hello!" -c 10

# Real run (be careful):
python messageBoombingV2.py -m "Hello!" -c 10 -d 0.5

# Use clipboard paste instead of typing (requires pyperclip)
python messageBoombingV2.py --clipboard -m "Long message..." -c 5
```

If you omit `--delay` on the command line the program will prompt you for the delay interactively.

## Safety & Responsible Use

This tool sends keystrokes and can interfere with other apps or users. Use it responsibly.

- Always use `--dry-run` first to verify intent.
- Keep the mouse at a safe distance during send; moving the mouse to the top-left corner will abort via PyAutoGUI's failsafe.
- Do not use this tool to spam or harass others. Use only on accounts, channels, or systems where you have permission.

## Troubleshooting

- If `pyautogui` is missing: `pip install pyautogui`.
- If `pyperclip` clipboard mode fails, install `pyperclip` (`pip install pyperclip`) or run without `--clipboard`.
- On some Linux distributions, PyAutoGUI may need additional display-related dependencies (e.g., `xclip`, `scrot`) — refer to PyAutoGUI docs.

## Continuous integration (GitHub Actions)

This repository includes a lightweight GitHub Actions workflow (`.github/workflows/ci.yml`) that performs a syntax check across Python files. The workflow keeps the "Get started with GitHub Actions" check green by executing a simple `python -m py_compile` on all tracked `.py` files.

How it helps

- Keeps the project healthy: simple static checks prevent syntax errors from reaching main branches.
- Fast and low-friction: the workflow does not run UI automation in CI and therefore avoids fragile runs.

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch.
3. Make changes and run `python -m py_compile` locally.
4. Open a pull request.

Please include a short description of changes and attach any relevant screenshots or logs if behavior changed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## A final note

This README aims to be readable and complete so anyone can understand the purpose, features, and safe usage of the project without reading source files. If you want, I can also add an example GIF showing the dry-run vs actual send (recorded locally), or expand the README with advanced examples.
# Auto Typing Script

This Python script uses the `pyautogui` library to automatically type and send the text "Hello World" repeatedly in any active text field. It waits for 3 seconds before starting, then continuously types and presses "Enter". This can be useful for automating simple tasks or testing purposes.

## Features

- Automatically types "Hello World" and presses "Enter".
- Simple and easy-to-use automation script.
- Uses the `pyautogui` library for keyboard control.

## Requirements

- Python 3.x
- `pyautogui` library

You can install the required library using:

```bash
pip install pyautogui
```

## Setting Up a Virtual Environment

For better package management and to avoid conflicts with your system environment, it's recommended to use a virtual environment.

### Steps:

1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

2. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

3. Install `pyautogui` inside the virtual environment:
    ```bash
    pip install pyautogui
    ```

4. Deactivate the virtual environment when you're done:
    ```bash
    deactivate
    ```

## How to Use

1. Clone or download the script.
2. Run the script in your terminal:
    ```bash
    python3 auto_typing_script.py
    ```
3. After the 3-second delay, the script will start typing "Hello World" and pressing "Enter" continuously.

### Example Output

The script will type:
```
Hello World
```
and press "Enter" repeatedly.

## License

This project is licensed under the MIT License.

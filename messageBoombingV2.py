"""Message bombing utility (safe, improved).

Features:
- Interactive prompts or CLI args
- Dry-run mode that prints actions instead of sending
- Clipboard paste option for large messages (`pyperclip`)
- PyAutoGUI failsafe enabled (move mouse to top-left to abort)
- Confirm before sending and countdown with cancel option
"""

from __future__ import annotations

import argparse
import sys
import time
import logging
from typing import Optional

try:
    import pyautogui
except Exception:
    print("pyautogui is required. Install with: pip install pyautogui")
    raise

try:
    import pyperclip
    _HAS_PYPERCLIP = True
except Exception:
    _HAS_PYPERCLIP = False

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

logging.basicConfig(format="%(message)s", level=logging.INFO)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Safe message sender using pyautogui")
    p.add_argument("-m", "--message", help="Message to send. If omitted, prompts interactively.")
    p.add_argument("-c", "--count", type=int, default=None, help="Number of times to send the message")
    p.add_argument("-d", "--delay", type=float, default=None, help="Delay in seconds between sends (if omitted you'll be prompted)")
    p.add_argument("--clipboard", action="store_true", help="Use clipboard paste instead of typing (requires pyperclip)")
    p.add_argument("--dry-run", action="store_true", help="Print actions instead of sending")
    p.add_argument("--type-interval", type=float, default=0.01, help="Interval between keystrokes when typing")
    p.add_argument("--no-confirm", action="store_true", help="Skip interactive confirmation")
    return p.parse_args(argv)


def prompt_for_message() -> str:
    while True:
        msg = input("\n..:: Enter the message to be bombed\t\t\t: ")
        if msg == "":
            yn = input("Message is empty. Proceed? (y/N): ").strip().lower()
            if yn == "y":
                return msg
            continue
        return msg


def prompt_for_count() -> int:
    while True:
        try:
            s = input("..:: Enter the number of times to send the message\t: ")
            n = int(s)
            if n <= 0:
                raise ValueError
            return n
        except ValueError:
            print("Please enter a positive integer.")


def prompt_for_delay() -> float:
    while True:
        try:
            s = input("..:: Enter the delay (in seconds) between each message\t: ")
            if s == "":
                return 0.0
            v = float(s)
            if v < 0:
                raise ValueError
            return v
        except ValueError:
            print("Please enter a non-negative number.")


def confirm_and_countdown(seconds: int = 5) -> bool:
    logging.info("\n\t\t==> Starting in %d seconds. Move mouse to top-left to abort.", seconds)
    for i in range(seconds, 0, -1):
        print(i, end="...\r")
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print()
            logging.info("Aborted by user during countdown.")
            return False
    print()
    return True


def send_message(message: str, count: int, delay: float, use_clipboard: bool, dry_run: bool, type_interval: float) -> None:
    if dry_run:
        logging.info("Dry-run: would send message %d times with %.3fs delay", count, delay)
        for i in range(1, count + 1):
            logging.info("[%d/%d] %r", i, count, message)
        return

    if use_clipboard and not _HAS_PYPERCLIP:
        logging.warning("pyperclip not available; falling back to typing mode")
        use_clipboard = False

    for i in range(1, count + 1):
        logging.info("Sending %d/%d", i, count)
        if use_clipboard:
            pyperclip.copy(message)
            pyautogui.hotkey("ctrl", "v")
        else:
            pyautogui.write(message, interval=type_interval)
        pyautogui.press("enter")
        time.sleep(delay)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    if args.message is None:
        message = prompt_for_message()
    else:
        message = args.message

    if args.count is None:
        count = prompt_for_count()
    else:
        if args.count <= 0:
            print("--count must be a positive integer")
            return 2
        count = args.count

    delay = args.delay if args.delay is not None else prompt_for_delay()

    if not args.no_confirm:
        print()
        print("Message preview:")
        print("-" * 40)
        print(message)
        print("-" * 40)
        ok = input(f"Send this message {count} times with {delay}s delay? (y/N): ").strip().lower()
        if ok != "y":
            print("Cancelled by user.")
            return 0

    if not confirm_and_countdown(5):
        return 0

    try:
        send_message(message, count, delay, args.clipboard, args.dry_run, args.type_interval)
    except pyautogui.FailSafeException:
        logging.info("Aborted by moving mouse to the top-left (failsafe).")
        return 0
    except KeyboardInterrupt:
        logging.info("Interrupted by user.")
        return 0

    logging.info("\n\n ..:: Message bombing completed ::..\n\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

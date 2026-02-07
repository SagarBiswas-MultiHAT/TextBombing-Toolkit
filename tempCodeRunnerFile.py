import sys
import time

try:
    import pyautogui
except Exception as e:
    print("pyautogui is required. Install with: pip install pyautogui")
    raise

# Enable failsafe (move mouse to top-left corner to abort) and small pause
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

def get_message():
    while True:
        msg = input("\n..:: Enter the message to be bombed\t\t\t\t: ").rstrip('\n')
        if msg == '':
            confirm = input("Message is empty. Send empty messages? (y/N): ").strip().lower()
            if confirm == 'y':
                return msg
            else:
                continue
        return msg

def get_positive_int(prompt):
    while True:
        try:
            count = int(input(prompt))
            if count <= 0:
                raise ValueError("The count must be a positive integer.")
            return count
        except ValueError as e:
            print(e)

def get_nonneg_float(prompt):
    while True:
        try:
            s = input(prompt).strip()
            if s == '':
                return 0.0

            # support suffixes like '500ms' or '2s'
            ls = s.lower()
            if ls.endswith('ms'):
                val = float(ls[:-2]) / 1000.0
            elif ls.endswith('s'):
                val = float(ls[:-1])
            else:
                val = float(ls)

            if val < 0:
                raise ValueError("The delay must be a non-negative number.")

            # Warn on very large delays and allow quick reinterpretation as milliseconds
            if val >= 10.0 and not ls.endswith('ms') and not ls.endswith('s'):
                resp = input(f"You entered a large delay ({val} seconds).\n" \
                             "Type 'y' to accept, 'ms' to treat the original number as milliseconds, or press Enter to re-enter: ").strip().lower()
                if resp == 'y':
                    return val
                if resp == 'ms':
                    # reinterpret original numeric string as milliseconds
                    val_ms = float(ls) / 1000.0
                    print(f"Interpreting {ls} as {val_ms} seconds (milliseconds).")
                    return val_ms
                # else loop to re-enter

            return val
        except ValueError as e:
            print(e)

def main():
    message = get_message()
    count = get_positive_int("..:: Enter the number of times to send the message\t: ")
    delay = get_nonneg_float("..:: Enter the delay (in seconds) between each message\t: ")

    print("\n\t\t==> Starting message bombing...")
    print("Place the cursor in the target input field/window now.")
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)
    print("\n\t!. BOMBING!")

    try:
        for i in range(count):
            pyautogui.write(message, interval=0.01)
            pyautogui.press("enter")
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n\n ..:: Interrupted by user ::..\n\n")
        sys.exit(0)
    except pyautogui.FailSafeException:
        print("\n\n ..:: Aborted by moving mouse to corner (failsafe) ::..\n\n")
        sys.exit(0)

    print("\n\n ..:: Message bombing completed ::..\n\n")

if __name__ == "__main__":
    main()

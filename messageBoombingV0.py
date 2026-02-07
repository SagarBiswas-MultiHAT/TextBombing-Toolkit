"""
Safe Typing Automation & Simulator
- Default behavior: simulates typing into internal GUI preview (no external messages).
- Provides dry-run, abort, randomization, logging, export.
- External auto-typing code is intentionally disabled/commented to avoid enabling misuse.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import threading
import random
import datetime

# Configuration (safety limits)
MAX_COUNT = 200           # hard cap to avoid accidental floods
MIN_DELAY = 0.0
MAX_DELAY = 60.0

class TypingSimulatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Safe Typing Automation & Simulator")
        root.geometry("800x560")
        self._running = False
        self._stop_event = threading.Event()
        self.log_lines = []

        self.build_ui()

    def build_ui(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill="both", expand=True)

        # Left: controls
        controls = ttk.LabelFrame(frm, text="Controls", padding=8)
        controls.grid(row=0, column=0, sticky="nsew", padx=(0,8), pady=4)
        frm.columnconfigure(0, weight=0)
        frm.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Message:").grid(row=0, column=0, sticky="w")
        self.msg_text = tk.Text(controls, width=40, height=6, wrap="word")
        self.msg_text.insert("1.0", "Hello, this is a test message.")
        self.msg_text.grid(row=1, column=0, columnspan=3, pady=(0,8))

        ttk.Label(controls, text="Count:").grid(row=2, column=0, sticky="w")
        self.count_var = tk.StringVar(value="5")
        self.count_entry = ttk.Entry(controls, textvariable=self.count_var, width=10)
        self.count_entry.grid(row=2, column=1, sticky="w")

        ttk.Label(controls, text="Delay (sec):").grid(row=3, column=0, sticky="w")
        self.delay_var = tk.StringVar(value="0.5")
        self.delay_entry = ttk.Entry(controls, textvariable=self.delay_var, width=10)
        self.delay_entry.grid(row=3, column=1, sticky="w")

        self.randomize_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(controls, text="Randomize delay (+/- 50%)", variable=self.randomize_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=(4,0))

        self.dry_run_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls, text="Dry-run (simulate only, default ON)", variable=self.dry_run_var).grid(row=5, column=0, columnspan=2, sticky="w", pady=(4,0))

        # Start / Abort / Export
        btn_frame = ttk.Frame(controls)
        btn_frame.grid(row=6, column=0, columnspan=3, pady=(8,0), sticky="w")

        self.start_btn = ttk.Button(btn_frame, text="Start (Simulate)", command=self.on_start)
        self.start_btn.grid(row=0, column=0, padx=(0,6))

        self.abort_btn = ttk.Button(btn_frame, text="Abort", command=self.on_abort, state="disabled")
        self.abort_btn.grid(row=0, column=1, padx=(0,6))

        ttk.Button(btn_frame, text="Export Log", command=self.export_log).grid(row=0, column=2, padx=(0,6))

        # Safety note
        safety = ("Safety: By default this app only types into the internal preview.\n"
                  "External auto-typing is intentionally disabled in this public demo.\n"
                  "Only enable external typing in a private, controlled environment.")
        ttk.Label(controls, text=safety, foreground="darkred", wraplength=320).grid(row=7, column=0, columnspan=3, pady=(10,0))

        # Right: preview and logs
        right = ttk.LabelFrame(frm, text="Preview & Logs", padding=8)
        right.grid(row=0, column=1, sticky="nsew")
        frm.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        ttk.Label(right, text="Typing Preview (internal):").grid(row=0, column=0, sticky="w")
        self.preview = tk.Text(right, height=10, state="normal", wrap="word")
        self.preview.grid(row=1, column=0, sticky="nsew", pady=(4,8))

        ttk.Label(right, text="Activity Log:").grid(row=2, column=0, sticky="w")
        self.log_box = tk.Text(right, height=10, state="normal", wrap="word")
        self.log_box.grid(row=3, column=0, sticky="nsew", pady=(4,0))

        # Progress
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress = ttk.Progressbar(right, variable=self.progress_var, maximum=100.0)
        self.progress.grid(row=4, column=0, sticky="ew", pady=(8,0))

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}"
        self.log_lines.append(line)
        self.log_box.insert("end", line + "\n")
        self.log_box.see("end")

    def validate_inputs(self):
        # message
        message = self.msg_text.get("1.0", "end").strip()
        if not message:
            raise ValueError("Message cannot be empty.")

        # count
        try:
            count = int(self.count_var.get())
            if count <= 0:
                raise ValueError("Count must be a positive integer.")
            if count > MAX_COUNT:
                raise ValueError(f"Count cannot exceed {MAX_COUNT}.")
        except ValueError:
            raise ValueError("Count must be a positive integer.")

        # delay
        try:
            delay = float(self.delay_var.get())
            if delay < MIN_DELAY or delay > MAX_DELAY:
                raise ValueError(f"Delay must be between {MIN_DELAY} and {MAX_DELAY} seconds.")
        except ValueError:
            raise ValueError("Delay must be a number (seconds).")

        return message, count, delay

    def on_start(self):
        try:
            message, count, delay = self.validate_inputs()
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            return

        # Confirm if not dry-run or if count is large
        if not self.dry_run_var.get() or count > 50:
            confirm = messagebox.askyesno("Confirm action",
                "You are about to run with external typing disabled in this demo.\n"
                "This demo defaults to dry-run (internal simulation). Continue?")
            if not confirm:
                return

        # Disable UI controls while running
        self.start_btn.config(state="disabled")
        self.abort_btn.config(state="normal")
        self._running = True
        self._stop_event.clear()
        self.progress_var.set(0)
        self.preview.delete("1.0", "end")
        self.log(f"Run started: count={count}, delay={delay}, dry_run={self.dry_run_var.get()}, randomize={self.randomize_var.get()}")

        # Run in background thread to keep UI responsive
        t = threading.Thread(target=self.run_typing, args=(message, count, delay, self.dry_run_var.get(), self.randomize_var.get()), daemon=True)
        t.start()

    def on_abort(self):
        if not self._running:
            return
        self.log("Abort requested by user.")
        self._stop_event.set()
        # UI will be reset by run thread

    def run_typing(self, message, count, delay, dry_run, randomize):
        try:
            for i in range(1, count + 1):
                if self._stop_event.is_set():
                    self.log("Run aborted before completion.")
                    break

                # compute sleep
                actual_delay = delay
                if randomize and delay > 0:
                    jitter = delay * 0.5
                    actual_delay = max(0, random.uniform(delay - jitter, delay + jitter))

                # Insert into internal preview (simulate typing character by character)
                self.simulate_typing_into_preview(message)

                # Log one "send"
                self.log(f"Simulated send #{i}: \"{message[:80]}{'...' if len(message)>80 else ''}\" (sleep {actual_delay:.2f}s)")

                # update progress
                self.progress_var.set((i / count) * 100.0)

                # Wait for the computed delay, checking for abort
                slept = 0.0
                step = 0.1
                while slept < actual_delay:
                    if self._stop_event.is_set():
                        break
                    time.sleep(min(step, actual_delay - slept))
                    slept += min(step, actual_delay - slept)
                if self._stop_event.is_set():
                    self.log("Run aborted during delay.")
                    break

            else:
                self.log("Run completed successfully.")

        finally:
            # Reset UI state
            self._running = False
            self._stop_event.clear()
            self.start_btn.config(state="normal")
            self.abort_btn.config(state="disabled")
            self.progress_var.set(0.0)

    def simulate_typing_into_preview(self, message, char_delay=0.01):
        # Inserts characters into preview widget to simulate typing effect.
        # This runs in a background thread — use Tk `after` to do safe UI updates.
        def char_inserter(idx=0):
            if idx < len(message):
                self.preview.insert("end", message[idx])
                self.preview.see("end")
                idx += 1
                # schedule next character
                self.root.after(int(char_delay * 1000), lambda: char_inserter(idx))
            else:
                # finished a message; append newline
                self.preview.insert("end", "\n")
                self.preview.see("end")
        # Start inserter on main thread
        self.root.after(0, char_inserter)

    def export_log(self):
        if not self.log_lines:
            messagebox.showinfo("Export log", "No log entries to export.")
            return
        path = filedialog.asksaveasfilename(title="Save log as", defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.log_lines))
            messagebox.showinfo("Export log", f"Log exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export failed", str(e))


def main():
    root = tk.Tk()
    app = TypingSimulatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

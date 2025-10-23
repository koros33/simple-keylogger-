# Safe demo: prints pressed keys to console only. No files, no email, no screenshots.
from pynput import keyboard

def on_press(key):
    try:
        print(f"Key pressed: {key.char}")
    except AttributeError:
        print(f"Special key pressed: {key}")

def on_release(key):
    # stop demo on Esc for convenience
    if key == keyboard.Key.esc:
        print("Stopping demo.")
        return False

print("Demo: keyboard listener started (press Esc to stop).")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

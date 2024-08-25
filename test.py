from pynput import mouse
import pyautogui

def on_click(x, y, button, pressed):
    if pressed:
        # Lấy tọa độ chuột trên màn hình
        print(f"Vị trí nhấp chuột trên màn hình: x={x}, y={y}")

def main():
    # Khởi động Listener để theo dõi sự kiện chuột
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

main()

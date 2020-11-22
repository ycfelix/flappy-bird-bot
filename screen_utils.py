import numpy as np
import pyautogui
import win32gui
from PIL import ImageGrab

def screenshot(hwnd):
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
        im = pyautogui.screenshot(region=(x, y, x1, y1))
        return np.array(im)
    else:
        print('Window not found!')


def screenshot_with_mouse(window_size=200):
    mouse_x, mouse_y = pyautogui.position()
    bbox = max(0, mouse_x - window_size), max(0, mouse_y - window_size), \
           min(1920, mouse_x + window_size), min(1080, mouse_y + window_size)
    pil_img = ImageGrab.grab(bbox=bbox)
    return np.array(pil_img)


def get_visble_window():
    windows = []
    win32gui.EnumWindows(lambda *arg: windows.append((hex(arg[0]), win32gui.GetWindowText(arg[0])))
    if win32gui.IsWindowVisible(arg[0]) else None, None)
    return windows


print(get_visble_window())
# cv2.imshow("test",)
# cv2.waitKey()

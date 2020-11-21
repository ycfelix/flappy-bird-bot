import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui

while True:
    mouse_x, mouse_y = pyautogui.position()
    bbox = max(0, mouse_x - 200), max(0, mouse_y - 200),min(1920, mouse_x + 200), min(1080, mouse_y + 200)
    pil_img = ImageGrab.grab(bbox=bbox)
    opencv_img = np.array(pil_img)
    cv2.imshow("n", opencv_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

import numpy as np
import cv2
from PIL import Image, ImageGrab
import pyautogui
from time import sleep

pyautogui.PAUSE = 0  # UNSAFE

startx, starty = 850, 67

stx, sty = 21, 37
endx, endy = 713, 531

w_game = endx - stx
h_game = endy - sty

w_cell = w_game / 7
h_cell = h_game / 5

x_c, y_c = w_cell / 2, h_cell / 2

a = dict()
x = 1
y = 1
prev = [0, 0]
for i in range(255, 0, -1):
    a[i] = [y, x]
    if i % 2 == 0:
        x += 1
    if x == 8:
        x = 1
        y += 1

cnt = 0
iterations = 0

levels = [16, 24, 32, 40, 60, 64, 64, 64, 72, 72]
level = 5
t_sleep = 8.1


def f(img):
    a = dict()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if a.get(img[i][j]) is None:
                a[img[i][j]] = 0
            a[img[i][j]] += 1
    x = max(a.values())
    c = 0
    ans = 0
    for i in a.keys():
        if a[i] == x:
            ans = i
        if a[i] <= 185:
            c += 1
    if c > 5:
        return -1
    return ans

while True:
    n1 = pyautogui.screenshot(region=(850, 60, 10, 10))
    n1 = np.array(n1)
    # n2 = pyautogui.screenshot(region=(847, 133, 10, 10))
    # n2 = np.array(n2)
    p1 = n1[:, :, 0]
    # p2 = n2[:, :, 0]
    p1 = f(p1)
    # p2 = f(p2)
    # if (p1 < 255 and p2 < 255 and (((p1 <= 185 or p2 <= 185) or not (249 <= n1[0][0][1] <= 251 and 249 <= n1[0][0][2] <= 251) or not (249 <= n2[0][0][1] <= 251 and 249 <= n2[0][0][2] <= 251)))) and cnt < 34:
    #     continue
    if p1 == -1:
        continue
    y, x = a[p1]
    x = stx + int(x_c + (x - 1) * w_cell)
    y = sty + int(y_c + (y - 1) * h_cell)
    pyautogui.moveTo(startx, starty)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x, y)
    pyautogui.mouseUp(button='left')
    sleep(0.15)
    cnt += 1
    if cnt == 35:
        if iterations + 1 == levels[level]:
            level += 1
            t_sleep = 10
            iterations = 0

        pyautogui.click(16, 60)
        sleep(t_sleep)
        pyautogui.click(16, 60)
        cnt = 0
        iterations += 1
        print('ITERATIONS', iterations)

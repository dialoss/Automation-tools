import numpy as np
import cv2
import pytesseract as pt
from PIL import Image, ImageGrab
import pyautogui
from time import sleep
import random
from mss import mss
import os

pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pyautogui.PAUSE = 0  # UNSAFE

frame_w = 30
frame_h = 30


def nears(img, i, j):
    p = lambda x: max(0, x - 1)
    pi = lambda x: min(x + 1, img.shape[0] - 1)
    pj = lambda x: min(x + 1, img.shape[1] - 1)

    a = [img[p(i)][j], img[p(i)][pj(j)], img[i][pj(j)], img[pi(i)][pj(j)],
         img[pi(i)][j], img[pi(i)][p(j)], img[i][p(j)], img[p(i)][p(j)]]
    cnt = 0
    if i == 0 or i == img.shape[1] - 1:
       cnt = 3
    if j == 0 or j == img.shape[0] - 1:
        cnt = 3
    if (i == 0 and j == 0) or (i == 0 and j == img.shape[0] - 1) or (i == img.shape[1] - 1 and j == img.shape[0] - 1):
        cnt = 5

    for x in a:
        if x > 230:
            cnt += 1
    if cnt >= 6:
        return True
    return False


def refill(img):
    p = lambda x: max(0, x - 1)
    pi = lambda x: min(x + 1, img.shape[0] - 1)
    pj = lambda x: min(x + 1, img.shape[1] - 1)

    new_img = img.copy()

    for i in range(img.shape[0]):
        # new_img[i][0] = 255
        # new_img[i][img.shape[1] - 1] = 255
        # new_img[0][i] = 255
        # new_img[img.shape[0] - 1][i] = 255
        for j in range(img.shape[1]):
            # if img[i][j][2] == 53 and img[i][j][1] == 32 and img[i][j][0] == 35:
            #     new_img[i][j][0] = 255
            #     new_img[i][pj(j)][0] = 255
            #     new_img[i][p(j)][0] = 255
            #     new_img[i][pj(pj(j))][0] = 255
            #     new_img[i][p(p(j))][0] = 255
            #     new_img[p(i)][j][0] = 255
            #     new_img[p(p(i))][j][0] = 255
            #     new_img[pi(i)][j][0] = 255
            #     new_img[pi(pi(i))][j][0] = 255
            # else:
            #     a = [new_img[p(i)][j][0], new_img[p(i)][pj(j)][0], new_img[i][pj(j)][0], new_img[pi(i)][pj(j)][0],
            #          new_img[pi(i)][j][0], new_img[pi(i)][p(j)][0], new_img[i][p(j)][0], new_img[p(i)][p(j)][0]]
            #     cnt = 0
            #     for x in a:
            #         if x > 230:
            #             cnt += 1
            #     if cnt >= 6:
            #         new_img[i][j][0] = 255
            #     if new_img[i][j][0] >= 190:
            #         new_img[i][j][0] = 255
            if img[i][j][2] == 53 or img[i][j][2] >= 130:
                new_img[i][j][0] = 255
            elif not (img[i][j][0] == img[i][j][1] == img[i][j][2]):
                new_img[i][j][0] = 255



    new_img = new_img[:, :, 0]
    return new_img


def get_bounds(img):
    xst, yst = frame_w, frame_h
    xend, yend = 0, 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if nears(img, i, j):
                continue
            if img[i][j] < 200:
                xst = min(xst, j)
                xend = max(xend, j)
                yst = min(yst, i)
                yend = max(yend, i)
    return xst, xend, yst, yend


def resized(img, side):
    new_img = np.full((16, 18), 255)
    xst, xend, yst, yend = get_bounds(img)

    w = abs(xst - xend) + 1
    h = abs(yst - yend) + 1
    posx = (18 - w) // 2
    posy = (16 - h) // 2

    for i in range(yst, yend + 1):
        for j in range(xst, xend + 1):
            new_img[min(15, posy + i - yst)][min(17, posx + j - xst)] = img[i][j]

    new_img = new_img.astype('uint8')
    return new_img


def string_to_int(s):
    n = ["", "", ""]
    for i in range(min(3, len(s))):
        if s[i] == 'A':
            n[i] = '4'
        elif s[i] == 'E':
            n[i] = '2'
        elif i == 0 and s[i] == 'B':
            n[i] = '1'
        elif s[i] == 'e':
            n[i] = '2'
        elif s[i] == '?' or s[i] == 'f':
            n[i] = '7'
        elif s[i] == 'a':
            n[i] = random.choice(['1', '3'])
        elif s[i] == 'g' or s[i] == 's' or s[i] == 'b' or s[i] == 'S':
            n[i] = '1'
        elif s[i] == 'z':
            n[i] = '2'
        elif s[i].isdigit():
            if s[i] == '8':
                n[i] = '1'
            else:
                n[i] = s[i]

    if n[0] != "" and n[2] != "":
        return [n[0], n[2]]
    else:
        return [n[0], n[1]]


retry = False

startx, starty = 600, 63

stx, sty = 30, 33
endx, endy = 487, 361

w_game = endx - stx
h_game = endy - sty

w_cell = w_game / 7
h_cell = h_game / 5

x_c, y_c = w_cell / 2, h_cell / 2
prev = ["", ""]


def predict(num):
    global retry, prev
    rotated = False
    angle = 0

    s = pt.image_to_string(num, config='--psm 13 --oem 3', lang='eng')
    n = s.strip()
    n = string_to_int(s)

    # while (not (len(n) == 2)) or (
    #         not (n[0].isdigit() and n[1].isdigit()) or (n[0].isdigit() and not n[1].isdigit()) or (
    #         not n[0].isdigit() and n[1].isdigit())) \
    #         or not (11 <= int(n[0] + n[1]) <= 59 or 81 <= int(n[0] + n[1]) <= 88):
    #     num = cv2.rotate(num, cv2.ROTATE_90_CLOCKWISE)
    #     s = pt.image_to_string(num, config='--psm 13 --oem 3', lang='eng')
    #     rotated = True
    #     angle += 1
    #     n = string_to_int(s)

    return n


def move_pieces(n):
    x, y = stx, sty
    if len(n) == 2 and n[0] != "" and n[1] != "":
        x = stx + int(x_c + (int(n[1]) - 1) * w_cell)
        y = sty + int(y_c + (int(n[0]) - 1) * h_cell)
    else:
        retry = True
        return False

    pyautogui.moveTo(startx, starty, 0.1)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.mouseUp(button='left')
    # if rotated:
    #     for i in range(angle):
    #         pyautogui.click(x, y)
    #         sleep(0.12)
    return True


cnt = 0
iterations = 0

with mss() as sct:
    while True:
        monitor = {"top": 42, "left": 582, "width": frame_w, "height": frame_h}
        screen = sct.grab(monitor)
        screen = np.array(screen)
        # cv2.imwrite(str(cnt) + "_original.png", screen)
        num = refill(screen)
        # cv2.imwrite(str(cnt) + "_refilled.png", num)
        num = resized(num, 1)
        # cv2.imwrite(str(cnt) + "_resized.png", num)

        n = predict(num)
        print(n)

        if move_pieces(n):
            cnt += 1

        if cnt == 35:
            pyautogui.click(8, 50)
            sleep(8)
            pyautogui.click(8, 50)
            cnt = 0
            iterations += 1
            print('ITERATIONS', iterations)

        sleep(0.2)

# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['image.cmap'] = 'gray'

mc_1 = cv2.imread('mc_1.jpg')
mc_2 = cv2.imread('mc_2.jpg')

#Выбераем Цветовое пространство
def select_colorsp(img, colorsp='gray'):
    # Преобразование в оттенки серого.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Разделить BGR.
    red, green, blue = cv2.split(img)
    # Преобразовать в HSV.
    im_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Разделить HSV.
    hue, sat, val = cv2.split(im_hsv)
    # Записываем каналы в словаре.
    channels = {'gray': gray, 'red': red, 'green': green,
                'blue': blue, 'hue': hue, 'sat': sat, 'val': val}

    return channels[colorsp]

#Служебная функция для отображения изображений размером 1 × 2
def display(im_left, im_right, name_l='Left', name_r='Right', figsize=(10, 7)):
    # Переключайте каналы для отображения, если RGB как matplotlib требует RGB.
    im_l_dis = im_left[..., ::-1] if len(im_left.shape) > 2 else im_left
    im_r_dis = im_right[..., ::-1] if len(im_right.shape) > 2 else im_right

    plt.figure(figsize=figsize)
    plt.subplot(121)
    plt.imshow(im_l_dis)
    plt.title(name_l)
    plt.axis(False)
    plt.subplot(122)
    plt.imshow(im_r_dis)
    plt.title(name_r)
    plt.axis(False)
    plt.show()

#Выполните пороговое значение
def threshold(img, thresh=127, mode='inverse'):
    im = img.copy()

    if mode == 'direct':
        thresh_mode = cv2.THRESH_BINARY
    else:
        thresh_mode = cv2.THRESH_BINARY_INV

    ret, thresh = cv2.threshold(im, thresh, 255, thresh_mode)

    return thresh

#Выполните анализ контуров для извлечения ограничивающих рамок
def get_bboxes(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Сортировка по площади контуров в порядке убывания.
    sorted_cnt = sorted(contours, key=cv2.contourArea, reverse = True)
    # Удалите максимальную площадь, самый внешний контур.
    sorted_cnt.remove(sorted_cnt[0])
    bboxes = []
    for cnt in sorted_cnt:
        x,y,w,h = cv2.boundingRect(cnt)
        cnt_area = w * h
        bboxes.append((x, y, x+w, y+h))
    return bboxes

#Служебная функция для рисования разхметки
def draw_annotations(img, bboxes, thickness=2, color=(0, 255, 0)):
    annotations = img.copy()
    for box in bboxes:
        tlc = (box[0], box[1])
        brc = (box[2], box[3])
        cv2.rectangle(annotations, tlc, brc, color, thickness, cv2.LINE_AA)

    return annotations


def morph_op(img, mode='open', ksize=5, iterations=1):
    im = img.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))

    if mode == 'open':
        morphed = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
    elif mode == 'close':
        morphed = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel)
    elif mode == 'erode':
        morphed = cv2.erode(im, kernel)
    else:
        morphed = cv2.dilate(im, kernel)

    return morphed

def get_filtered_bboxes(img, min_area_ratio=0.001):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Отсортируем контуры по площади, от большего к меньшему.
    sorted_cnt = sorted(contours, key=cv2.contourArea, reverse = True)
    # Удаляем максимальную площадь, самый внешний контур.
    sorted_cnt.remove(sorted_cnt[0])
    # Container to store filtered bboxes.
    bboxes = []
    # Область изображения.
    im_area = img.shape[0] * img.shape[1]
    for cnt in sorted_cnt:
        x,y,w,h = cv2.boundingRect(cnt)
        cnt_area = w * h
        # Удалите очень мелкие дефекты.
        if cnt_area > min_area_ratio * im_area:
            bboxes.append((x, y, x+w, y+h))
    return bboxes

#Выбираем цветовое пространство
# gray_mc1 = select_colorsp(mc_1)
# #Выполнить пороговое значение
# thresh_stags = threshold(gray_mc1, thresh=110)
#

# Display.
# display(mc_1, thresh_stags,
#         name_l='Stags original infrared',
#         name_r='Thresholded Stags',
#         figsize=(20, 14))

# Выполняем морфологическую операцию.
# morphed_stags = morph_op(thresh_stags)

# # Display.
# display(thresh_stags, morphed_stags,
#         name_l='Thresholded Stags',
#         name_r='Morphological Operations Result',
#         figsize=(20,14))
# bboxes = get_bboxes(morphed_stags)
#
# ann_morphed_stags = draw_annotations(thresh_stags, bboxes, thickness=5, color=(0,0,255))
# Display.
# display(mc_1, ann_morphed_stags,
#         name_l='Annotating Thresholded Stags',
#         name_r='Annotating Morphed Stags',
#         figsize=(20,14))
# bboxes = get_filtered_bboxes(thresh_stags, min_area_ratio=0.001)
#
# filtered_ann_stags = draw_annotations(mc_1, bboxes, thickness=5, color=(0, 0, 255))
#
# Display.
# display(mc_1, filtered_ann_stags,
#         name_l='Annotating Thresholded Stags',
#         name_r='Annotation After Filtering Smaller Boxes',
#         figsize=(20, 14))

#Создание цветовой маски
# def get_color_mask(img, lower=[0, 0, 0], upper=[0, 255, 255]):
#     img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     low = np.array(lower)
#     up = np.array(upper)
#     mask = cv2.inRange(img_hsv, low, up)
#     inv_mask = 255 - mask
#
#     return inv_mask
#
#
# mask_mc_1 = get_color_mask(mc_1,
#                               lower=[0, 211, 111],
#                               upper=[16, 255, 255])
#
# # Морфологическая операция, значение по умолчанию - 'open'.
# morphed_berries = morph_op(mask_mc_1)
#
# # Контурный анализ.
# bboxes = get_filtered_bboxes(morphed_berries,
#                              min_area_ratio=0.0005)
#
# # Рисуем разметку.
# ann_berries = draw_annotations(mc_1, bboxes,
#                                thickness=2,
#                                color=(255, 0, 0))
#
# # Display.
# display(mc_1, ann_berries,
#         name_l='Strawberries',
#         name_r='Annotated Strawberries',
#         figsize=(20, 14))

#4.4 Анализ цветового пространства HSV
# RGB colorspace.
blue_boxes = select_colorsp(mc_1, colorsp='blue')
green_boxes = select_colorsp(mc_1, colorsp='green')
red_boxes = select_colorsp(mc_1, colorsp='red')
gray_boxes = select_colorsp(mc_1, colorsp='gray')
#
# # Display.
# plt.figure(figsize=(20, 7))
# plt.subplot(221);
# plt.imshow(blue_boxes);
# plt.title('Blue');
# plt.axis(False);
# plt.subplot(222);
# plt.imshow(green_boxes);
# plt.title('Green');
# plt.axis(False);
# plt.subplot(223);
# plt.imshow(red_boxes);
# plt.title('Red');
# plt.axis(False);
# plt.subplot(224);
# plt.imshow(gray_boxes);
# plt.title('Gray');
# plt.axis(False);

# HSV colorspace.
hue_boxes = select_colorsp(mc_1, colorsp='hue')
sat_boxes = select_colorsp(mc_1, colorsp='sat')
val_boxes = select_colorsp(mc_1, colorsp='val')

# Display.
# plt.figure(figsize=(20, 7))
# plt.subplot(221);
# plt.imshow(hue_boxes);
# plt.title('Hue');
# plt.axis(False);
# plt.subplot(222);
# plt.imshow(sat_boxes);
# plt.title('Saturation');
# plt.axis(False);
# plt.subplot(223);
# plt.imshow(val_boxes);
# plt.title('Lightness');
# plt.axis(False);
# plt.subplot(224);
# plt.imshow(gray_boxes);
# plt.title('Gray');
# plt.axis(False);
# plt.show()

boxes_thresh = threshold(sat_boxes, thresh=70)
morphed_boxes = morph_op(boxes_thresh, mode='open')
bboxes = get_filtered_bboxes(morphed_boxes)
ann_boxes = draw_annotations(mc_1, bboxes, thickness=4, color=(0, 0, 255))

plt.figure(figsize=(10, 7))
plt.subplot(211);
plt.imshow(mc_1[..., ::-1]);
plt.title('Boxes Original');
plt.axis(False);
plt.subplot(212);
plt.imshow(ann_boxes[..., ::-1]);
plt.title('Annotated Boxes');
plt.axis(False);
plt.show()
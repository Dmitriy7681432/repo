# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Читаем картинку как чб
cb_img = cv2.imread("check.png",0)
# cb_img = cv2.imread("mc_1.jpg",0)
# Выводим массив, представляющий картинку
# print(cb_img)
#
# # Выводим значение самого первого пикселя (верх-лево)
# print(cb_img[0,0])
# # Выводим значение первого пикселя слева от чёрной зоны
# print(cb_img[0,6])


# Обрезка картинки
img_mc_1 = cv2.imread("mc_2.jpg",cv2.IMREAD_COLOR)
img_mc_1_rgb = cv2.cvtColor(img_mc_1, cv2.COLOR_BGR2RGB)
# plt.imshow(img_mc_1_rgb)
# plt.show()

# кропнутый регион = область загруженной картинки
# c 200 по 400 строку (или Y, если хотите)
# и 300 по 600 колонку (или X, если хотите)
# cropped_region = img_mc_1_rgb[200:1800, 300:2600]
# cropped_region = img_mc_1_rgb[400:1750,2000:3400]
cropped_region = img_mc_1_rgb[:,:]

# plt.imshow(cropped_region)
# plt.show()

resized_cropped_region_2x = cv2.resize(cropped_region,None,fx=1, fy=1)

# Желаемая ширина и высотва
# resized_cropped_region = cv2.resize(cropped_region,
# 	                                   dsize = (800, 1200),
# 	                                   interpolation = cv2.INTER_AREA)

# Приводим картинку к RGB для того, чтобы сохранить в цветном режиме
resized_cropped_region_2x = resized_cropped_region_2x[:,:,::-1]

plt.imshow(resized_cropped_region_2x)
plt.show()

# Отражение картинки
# img_NZ_rgb_flipped_horz = cv2.flip(resized_cropped_region_2x, 1)
# img_NZ_rgb_flipped_vert = cv2.flip(resized_cropped_region_2x, 0)
# img_NZ_rgb_flipped_both = cv2.flip(resized_cropped_region_2x, -1)

# Отображение сразу 4 картинок
# plt.figure(figsize=[18,5])
# plt.subplot(141);plt.imshow(img_NZ_rgb_flipped_horz);plt.title("Horizontal Flip");
# plt.subplot(142);plt.imshow(img_NZ_rgb_flipped_vert);plt.title("Vertical Flip")
# plt.subplot(143);plt.imshow(img_NZ_rgb_flipped_both);plt.title("Both Flipped")
# plt.subplot(144);plt.imshow(resized_cropped_region_2x);plt.title("Original")
# plt.show()




# Сохраняем картинку
# cv2.imwrite("26_logic.jpg", img_NZ_rgb_flipped_vert)
# cv2.imwrite("27_logic.jpg", img_NZ_rgb_flipped_both)

# Посмотрим на сокранённую картинку (тут-то нам и пригодится подгруженный PIL)
# im = Image.open('26_logic.jpg')
# im.show()

# -*- coding: utf-8 -*-
import numpy as np
import cv2
import matplotlib.pyplot as plt
# читать входное изображение
img = cv2.imread("mc_3.jpg")
# конвертировать из BGR в RGB, чтобы мы могли построить график с помощью matplotlib
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# отключить оси x и y
plt.axis('off')
# показать изображение
plt.imshow(img)
plt.show()
# получить форму изображения
rows, cols, dim = img.shape
# матрицы преобразования для сдвига
# сдвиг, примененный к оси x
M = np.float32([ [1, 0.5, 0],
               [0, 1  , 0],
              [0, 0  , 1] ])
# сдвиг, примененный к оси Y
# M = np.float32([ [1,   0, 0],
#                 [0.5, 1, 0],
#                 [0,   0, 1] ])
# применяем перспективное преобразование к изображению
sheared_img = cv2.warpPerspective(img,M,(int(cols*1.5),int(rows*1.5)))
# отключить оси x и y
plt.axis('off')
# show the resulting image
plt.imshow(sheared_img)
plt.show()
# сохраняем получившееся изображение на диск
plt.imsave("mc_3_change.jpg", sheared_img)
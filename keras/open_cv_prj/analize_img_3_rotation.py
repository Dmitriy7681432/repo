# -*- coding: utf-8 -*-
import numpy as np
import cv2
import matplotlib.pyplot as plt
# читать входное изображение
img = cv2.imread("mc_3.jpg")
# преобразовать из BGR в RGB, чтобы можно было построить график с помощью matplotlib
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# отключить оси x и y
plt.axis('off')
# показать изображение
plt.imshow(img)
plt.show()
# получить форму изображения
rows, cols, dim = img.shape
# угол от градуса до радиана
angle = np.radians(10)
# матрица преобразования для вращения
M = np.float32([ [np.cos(angle), -(np.sin(angle)), 0],
              [np.sin(angle), np.cos(angle), 0],
              [0, 0, 1] ])
# применяем перспективное преобразование к изображению
rotated_img = cv2.warpPerspective(img, M, (int(cols),int(rows)))
# отключить оси x и y
plt.axis('off')
# показать получившееся изображение
plt.imshow(rotated_img)
plt.show()
# сохраняем получившееся изображение на диск
plt.imsave("mc_3_change_rotation.jpg", rotated_img)
# -*- coding: utf-8 -*-
# добавим необходимый пакет с opencv
import cv2
import matplotlib.pyplot as plt

# загружаем изображение и отображаем его
image = cv2.imread("mc_2.jpg")
final_wide = 1200
r = float(final_wide) / image.shape[1]
dim = (final_wide, int(image.shape[0] * r))

# уменьшаем изображение до подготовленных размеров
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
resized= resized[:,:,::-1]
cv2.imshow("Resize image", resized)
cv2.waitKey(0)
plt.imshow(resized)
plt.imsave("mc_2_change_decrease.jpg", resized)

# -*- coding: utf-8 -*-
# https://www.youtube.com/watch?v=oCXh_GFMmOE
import os
#Для того чтобы не скачивать CUDA for GPU Tenssorflow и
# не выходило предупреждения перед запуском программы
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist # библиотека базы выборок mnist (коллекция рукописных цифр)
from tensorflow import keras
from tensorflow.keras.layers import Dense,Flatten

(x_train, y_train), (x_test, y_test) = mnist.load_data()

#Стандартизация данных
x_train = x_train/ 255
x_test = x_test/ 255

y_train_cat = keras.utils.to_categorical(y_train, 10)
y_test_cat = keras.utils.to_categorical(y_test, 10)

#Отображение первых 25 изображений из обучающей выборки
plt.figure(figsize=(10,5))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(x_train[i], cmap=plt.cm.binary)
plt.show()
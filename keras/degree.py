# -*- coding: utf-8 -*-
# https://www.youtube.com/watch?v=BQg9OZdzLLE
import os
#Для того чтобы не скачивать CUDA for GPU Tenssorflow и
# не выходило предупреждения перед запуском программы
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense


c = np.array([-40,-10,0,8,15,22,38])
f = np.array([-40,-14,32,46,59,72,100])

# Создаем модель многослойной нейронной сети
model =keras.Sequential()
#Добавляем слой
model.add(Dense(units=1, input_shape=(1,), activation='linear'))
# Критерий качества компиляции
model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(0.1))
# Запуск
history = model.fit(c,f,epochs=500,verbose=0)

plt.plot(history.history['loss'])
plt.grid(True)
plt.show()
# На вход подаем градусы цельсия
print(model.predict([100]))
print(model.get_weights())

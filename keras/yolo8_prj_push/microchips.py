# -*- coding: utf-8 -*-
from ultralytics import YOLO
#обучение
# model = YOLO('yolov8n.yaml')
# model = YOLO('yolov8n.pt')

# results = model.train(data='microchips.yaml', epochs=300)

#проверка
# model = YOLO("D:\repo\keras\yolo8_prj\runs\detect\train4\weights\best.pt")
model = YOLO("last_memory_1.pt")

# results = model('3_memory.jpg')
#
# names_dict = results[0].names
# probs = results[0].probs
#
# print(names_dict)
# print(probs)
# results.show()
# success = model.export(format='onnx')

model.predict(source = "11.jpg",show=True,save=True,show_labels = True,show_conf=True,conf =0.5,save_txt=False,save_crop=False,line_width=2)
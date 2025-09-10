# -*- coding: utf-8 -*-
import json,serial.tools.list_ports
ports = serial.tools.list_ports.comports()

serial_number = 0
flag =0
# Считывание серийного номера
for port in ports:
    serial_number = port.serial_number[:3]

# Чтение данных с configs
with open('configs.json','r') as file_configs:
    configs = json.load(file_configs)
    cnt = int(configs.get('count_write_json'))
# Проверка на уже имеющиеся серийные номера
for i in configs.values():
    if i == serial_number:
        flag = 1

# Изменение структуры данных, считанных с configs
configs[f'serial_number{cnt+1}'] = serial_number
configs['count_write_json'] = str(cnt+1)

# Запись данных в oconfigs
if serial_number !=0 and flag ==0:
    with open('configs.json','w') as file_configs:
        json.dump(configs,file_configs,ensure_ascii=False,indent=4)
        print('Записан новый серийный номер com_port')
else:
    print('Есть уже такой com_port или не определены com_port')


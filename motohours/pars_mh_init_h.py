# -*- coding: utf-8 -*-
# Парсинг файла со структорой наработки и выводит результат в виде списка наименований параметров,
# хранящихся в памяти
import re
class ParsInitMh():
    def __init__(self,station):
        self.station = station.lower()

    def pars(self):
        temp_begin = 'mh_flash'
        temp_end ='mh_flash_t'
        result_list = []
        with open(f'headers_mh/mh_init_{self.station}.h','r',encoding='utf-8') as file:
            # res = file.read().splitlines()
            res = file.read()
            indx_begin = res.find(temp_begin)
            indx_end = res.find(temp_end)
            res = res[indx_begin:indx_end]
            # Выводит строки после симвоал // и до символа /n
            res= re.findall(r'//(.*)', res)
            for result in res:
                # Заменяет в начале один пробел на пустую строку
                result = re.sub(r"^\s+", "", result)
                result_list.append(result)
        return result_list

# pars_obj = ParsInitMh('SES200M')
# print(pars_obj.pars())



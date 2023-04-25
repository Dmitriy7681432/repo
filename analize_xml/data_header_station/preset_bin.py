## @file preset_bin.py
#  @brief Автоматическая генерация preset.bin TAKI00039-01 81 16.vsdx Python 3.7.9
#  @details
#  @date 14.03.2022
#  @author Никонов С.Ю.
#  @version 0.0.1
#  @version 0.0.2 22.03.2022 С бинарной шапкой

# Пример запуска
# /etc/Python37/python \
#     py_scripts/preset_bin.py \
#     -station $(STATION) \
#     -control_block $(CONTROL_BLOCK) \
#     station_data/params.xml \
#     src/generated/preset.bin

from __future__ import annotations

import lxml.etree

import sys
import datetime
import io
import argparse
import struct
import html
import binascii

from typing import Union, Iterator


def chunked_bytes(size: int, source: bytearray) -> Iterator[str]:
    for i in range(0, len(source), size):
        yield "".join([f"{x:02x}" for x in source[i : i + size]])


def main():
    # Смена кодировки вывода на utf-8
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    # Печать на экран названия текущего скрипта
    print("preset_bin.py")

    # Создание парсера аргументов
    # Чтобы посмотреть какие есть аргументы, нужно запустить скрипт с параметром --help
    # Например, python command_names.py --help
    parser = argparse.ArgumentParser()
    # аргумент -station <station>
    parser.add_argument("-station")
    # аргумент -control_block <control_block>
    parser.add_argument("-control_block")
    # аргумент <params_xml_filename> - входящий файл
    parser.add_argument("params_xml_filename", help="params.xml filename with path")
    # аргумент <out_filename> - исходящий файл
    parser.add_argument("out_filename", help="out filename with path")
    # аргумент -add_header - добавить шапку
    parser.add_argument("-add_header", help="adds header", action="store_true")
    # аргумент -git_commit - git commit hash субмодуля station_data
    parser.add_argument("-git_commit", help="git commit hash of station_data submodule")
    # Парсинг аргументов
    args = parser.parse_args()

    # Станция из аргументов
    station = args.station
    # Контрольный блок из аргументов
    control_block = args.control_block

    # Открытие входящего файла
    with open(args.params_xml_filename, encoding="utf-8") as f:
        xml_string = f.read()

    # Печать на экран информации о именах исходных и выходных файлов
    print(f"{args.params_xml_filename} -> {args.out_filename}")

    # Загрузка xml файла в парсинг XML. Библиотека lxml
    doc = lxml.etree.XML(xml_string.encode())

    # XPath для поиска всех уставок
    xpath = f'/station/presets/setting/products[1]/{station}[@cb="{control_block}"]/parent::*/parent::*'
    print(f"XPath для уставок: {xpath}")
    # Поиск всех уставок
    par_ev_lims = doc.xpath(xpath)

    # List в который записываются все нужные параметры
    l_presets: list[dict[str, Union[int, float]]] = []

    # Бинарный файл начинается с 0xA5A55A5A
    out_byte_array = bytearray(0xA5A55A5A.to_bytes(length=4, byteorder="little"))
    out_data_array = bytearray()

    # Инициализация переменных количеств
    n_presets = 0
    # Цикл по всем параметрам
    for pel in par_ev_lims:
        # Для debug. Вывод всех параметров с аттрибутами
        # print(
        #     pel.get("number"),
        #     pel.get("min"),
        #     pel.get("default_value"),
        #     pel.get("max"),
        #     pel.get("ctype"),
        # )

        # Записываем 4 значения по порядку min, default, default, max
        for v in [
            pel.get("min"),
            pel.get("default_value"),
            pel.get("default_value"),
            pel.get("max"),
        ]:
            # Если тип int
            if pel.get("ctype") == "int":
                if pel.get("dimension") == "с":
                    try:
                        v_int = int(round(float(v) * 1000))
                    except ValueError as e:
                        repr_pel = repr(
                            html.unescape(lxml.etree.tostring(pel).decode())
                        )
                        raise ValueError(
                            f'Тип {pel.get("ctype")} не соответствует числу {v}. {repr_pel}'
                        ) from e

                else:
                    try:
                        v_int = int(v)
                    except ValueError as e:
                        repr_pel = repr(
                            html.unescape(lxml.etree.tostring(pel).decode())
                        )
                        raise ValueError(
                            f'Тип {pel.get("ctype")} не соответствует числу {v}. {repr_pel}'
                        ) from e

                out_data_array += v_int.to_bytes(
                    length=4, byteorder="little", signed=True
                )

            # Если тип float
            elif pel.get("ctype") == "float":
                try:
                    v_float = float(v)
                except ValueError as e:
                    repr_pel = repr(html.unescape(lxml.etree.tostring(pel).decode()))
                    raise ValueError(
                        f'Тип {pel.get("ctype")} не соответствует числу {v}. {repr_pel}'
                    ) from e
                out_data_array += struct.pack("f", v_float)

            # Иначе вылетаем с ошибкой
            else:
                raise ValueError(f'Тип {pel.get("ctype")} не обрабатывается')
        n_presets += 1

    # Печать на экран количества параметров
    print(f"кол-во уставок={n_presets}")

    

    # Добавляем шапку файла если есть опция header
    header_bytes = bytearray()
    if args.add_header:
        # CRC
        crc = binascii.crc32(out_data_array)
        print("CRC32(data)=", hex(crc))
        header_bytes += crc.to_bytes(length=4, byteorder="little", signed=False)

        # Date
        now = datetime.datetime.now()
        # Date year
        year = str(now.year)
        year_bytes = 0
        weights = [1, 0, 3, 2]
        for i, ch in enumerate(year):
            year_bytes += (16 ** weights[i]) * int(ch)

        # Date month
        month = 0
        s_month = str(now.month)
        for i, ch in enumerate(s_month):
            month += (16 ** weights[i + 2 - len(s_month)]) * int(ch)

        # Date day
        day = 0
        s_day = str(now.day)
        for i, ch in enumerate(s_day):
            day += (16 ** weights[i + 2 - len(s_day)]) * int(ch)

        date_bytes = (
            year_bytes.to_bytes(length=2, byteorder="little", signed=False)
            + month.to_bytes(length=1, byteorder="little", signed=False)
            + day.to_bytes(length=1, byteorder="little", signed=False)
        )
        print("Date hex=" + ":".join([f"{x:02x}" for x in date_bytes]))
        header_bytes += date_bytes

        # Time
        # Time hours
        hours = 0
        s_hours = str(now.hour)
        for i, ch in enumerate(s_hours):
            hours += (16 ** weights[i + 2 - len(s_hours)]) * int(ch)

        # Time minutes
        minutes = 0
        s_minutes = str(now.minute)
        for i, ch in enumerate(s_minutes):
            minutes += (16 ** weights[i + 2 - len(s_minutes)]) * int(ch)

        # Time seconds
        seconds = 0
        s_seconds = str(now.second)
        for i, ch in enumerate(s_seconds):
            seconds += (16 ** weights[i + 2 - len(s_seconds)]) * int(ch)

        time_bytes = (
            hours.to_bytes(length=1, byteorder="little", signed=False)
            + minutes.to_bytes(length=1, byteorder="little", signed=False)
            + seconds.to_bytes(length=1, byteorder="little", signed=False)
            + (0).to_bytes(length=1, byteorder="little", signed=False)
        )
        print("Time hex=" + ":".join([f"{x:02x}" for x in time_bytes]))
        header_bytes += time_bytes

        # Git commit from input arguments
        git_commit = bytes.fromhex(args.git_commit)[:4]
        print("Git commit=" + "".join([f"{x:02x}" for x in git_commit]))
        header_bytes += git_commit

        # Флаг from_display. 0 если запись с компьютера
        header_bytes += (0).to_bytes(length=4, byteorder="little", signed=False)

        # Длина данных в количестве struct'ов (struct из 4х полей)
        header_bytes += n_presets.to_bytes(length=4, byteorder="little", signed=False)

    out_byte_array += header_bytes
    # print(list(chunked(4, "asdfasdfasdf")))
    print(
        "Шапка файла до данных:",
        " ".join(chunked_bytes(4, out_byte_array)),
    )

    out_byte_array += out_data_array

    # Сохраняем новый файл
    with open(args.out_filename, "wb") as f:
        f.write(out_byte_array)


if __name__ == "__main__":
    main()

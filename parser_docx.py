# -*- coding: utf-8 -*-
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
# https://docs-python.ru/packages/modul-python-docx-python/obekt-table/
doc  = Document()
# добавляем пустую таблицу 2х2 ячейки
items = (
    (7, '1024', 'Плюшевые котята'),
    (3, '2042', 'Меховые пчелы'),
    (1, '1288', 'Ошейники для пуделей'),
)
# добавляем таблицу с одной строкой
# для заполнения названий колонок
table = doc.add_table(1, len(items[0]))
table.style = 'Table Grid'
# Получаем строку с колонками из добавленной таблицы
head_cells = table.rows[0].cells
# for i in head_cells:
#     print(i.text)
for i, item in enumerate(['Кол-во', 'ID', 'Описание']):
    p = head_cells[i].paragraphs[0]
    # название колонки
    p.add_run(item).bold = True
    # выравниваем посередине
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
# table = doc.add_table(rows=2, cols=2)
# cell = table.cell(1, 1)
# cell.text = 'Бык'
# rc = cell.paragraphs[0].runs[0]

# row = table.rows[1]
# # запись данных в ячейки
# row.cells[0].text = 'Заяц'
# row.cells[1].text = 'Волк'

# rc.font.name = 'Arial'
# rc.font.bold = True
doc.save('test.docx')

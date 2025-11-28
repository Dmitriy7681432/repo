# -*- coding: utf-8 -*-
import sys,re,struct,PyQt5.Qt
import time

from PyQt5.QtWidgets import (QWidget, QPushButton, QStackedWidget,
                             QHBoxLayout, QVBoxLayout, QApplication, QAction, QMainWindow)

from PyQt5 import QtCore, QtGui, QtWidgets
from class_read_data import Connect,Calibrator
from debug import *
from PyQt5.QtCore import pyqtSignal


class MyWidget(QWidget):
    keyPressed = QtCore.pyqtSignal(int)

    def keyPressEvent(self, event):
        super(MyWidget, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

class Id:
    id_lst = []
class TableFocus(QtWidgets.QTableView,Id):
    keyPressed = QtCore.pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.id = None
        self.id_lst = Id.id_lst

    def keyPressEvent(self, event):
        super(TableFocus, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())
    def event(self, e):
        if e.type() == QtCore.QEvent.Shortcut:
            printf('id',self.id)
            if self.id == e.shortcutId():
                self.id_lst.append(self.id)
                self.setFocus(QtCore.Qt.ShortcutFocusReason)
                # self.setFocus(QtCore.Qt.MouseFocusReason)
                return True
        return QtWidgets.QTableView.event(self,e)


class Unit(MyWidget,QWidget):
    # keyPressed = QtCore.pyqtSignal(int)
    cal_signal = pyqtSignal(int)

    def __init__(self, data_dict,data, unit, height_desktop):
        super().__init__()
        self.initUI(data_dict,data,unit, height_desktop)
        # self.keyPressed.connect(self.on_key)

    # def keyPressEvent(self, event):
    #     super(Unit, self).keyPressEvent(event)
    #     self.keyPressed.emit(event.key())

    # def on_key(self, e):
    #
    #     # self.table.keyPressEvent = self.keyPressEvent
    #     printff('keyPressEvent')
    #     # super(Unit,self).keyPressEvent(e)
    #
    #     if e.key() == PyQt5.Qt.Qt.Key_Up:
    #         printff('UP',e.text())
    #         # self.table.focusNextChild()
    #
    #     if e.key() == PyQt5.Qt.Qt.Key_Down:
    #         printff('DOWD',e.text())
    def initUI(self,data_dict, data,unit,height_desktop):
        # Шрифт
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        # font.setBold(True)
        # font.setWeight(75)


        # Порт
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.page.setGeometry(QtCore.QRect(0,0,0,0))

        # self.centralwidget = centr
        # self.centralwidget(self.page)
        # self.centralwidget.setObjectName("centralWidget")
        # self.horizontWidget = QtWidgets.QWidget(self.page)
        # self.horizontWidget.setGeometry(QtCore.QRect(20, 20, 210, 40))
        # self.horizontWidget.setObjectName("horizontWidget")
        self.horizontLayout = QtWidgets.QVBoxLayout(self.page)
        self.horizontLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout.setObjectName("horizontLayout")
        # self.centralwidget.addLayout(self.horizontLayout)
        # self.horizontLayout.addStretch(1)


        # for i in data_dict['preset'].items():
        #     printff(i[1][0])

        len_data_dict =len(data_dict[data].items())

        count =0; count1=0;count2=0
        self.data_tab =QtWidgets.QTabWidget()
        self.model = QtGui.QStandardItemModel()
        # table = QtWidgets.QTableView()
        self.table = TableFocus()
        # table.id = table.grabShortcut(
        #     QtGui.QKeySequence(PyQt5.Qt.Qt.Key_Up))
        # table.id = table.grabShortcut(
        #     QtGui.QKeySequence(PyQt5.Qt.Qt.Key_Down))
        # self.table.keyPressEvent = self.keyPressEvent

        # self.widget1 = MyWidget()


        self.lst_table = []
        self.lst_model = []
        for i in data_dict[data].items():

            item1 = QtGui.QStandardItem(i[0])
            item2 = QtGui.QStandardItem(i[1][0])
            if data == 'preset':
                if i[1][1] == 'int':
                    self.item3 = QtGui.QStandardItem(str(0))
                else:
                    self.item3 = QtGui.QStandardItem(str(0.0))
            else:
                self.item3 = QtGui.QStandardItem(str(0.0))


            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            self.item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item1.setEditable(False)
            item2.setEditable(False)
            self.item3.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            item1.setSelectable(False)
            item2.setSelectable(False)
            self.item3.setSelectable(False)

            self.model.appendRow([item1,item2,self.item3])
            self.table.setModel(self.model)
            self.table.setRowHeight(count, 12)
            count +=1
            count2 +=1
            # cnt_elem = round((table.size().height()/table.rowHeight(0))+0.5)
            self.cnt_elem = round((height_desktop/2/self.table.rowHeight(0))+0.5)
            # printff(cnt_elem)
            if count ==self.cnt_elem or count2 == len_data_dict:
                self.table.setColumnWidth(0, 190)
                self.table.setColumnWidth(1, 520)
                self.table.setColumnWidth(2, 154)
                self.table.setRowHeight(0,20)
                self.model.setHorizontalHeaderLabels(['Обозначение', 'Наименование', 'Значение'])
                self.table.setFont(font)
                self.table.verticalHeader().setVisible(False)
                count1 +=1
                self.data_tab.addTab(self.table,f"Вкладка {count1}")
                self.lst_table.append(self.table)
                self.lst_model.append(self.model)
                count =0
                self.model = QtGui.QStandardItemModel()
                # table = QtWidgets.QTableView()
                self.table = TableFocus()
                # table.id = table.grabShortcut(
                #     QtGui.QKeySequence(PyQt5.Qt.Qt.Key_Up))
                # table.id = table.grabShortcut(
                #     QtGui.QKeySequence(PyQt5.Qt.Qt.Key_Down))


        self.index_data_tab = self.data_tab.currentIndex()
        for i in range(0,self.data_tab.count()):
            self.lst_table[i].clicked.connect(self.selectRow1)
            self.lst_model[i].itemChanged.connect(self.changedValue)
            self.lst_table[i].entered.connect(self.enteredValue)
            self.lst_table[i].pressed.connect(self.pressedValue)
            self.lst_table[i].activated.connect(self.activatedValue)
            self.lst_table[i].selectRow(0)
            self.lst_table[i].keyPressed.connect(self.on_key)
            # table.activated
        self.data_tab.currentChanged.connect(self.selectDataTab)

        self.readData_flag = 0
        # Вкладки
        self.data_tab.setStyleSheet('background-color:rgb(220,254,225);')\
                               # gridline-color:gray;')
        self.horizontLayout.addWidget(self.data_tab)
        self.horizontLayout.setAlignment(QtCore.Qt.AlignHCenter)
        # self.horizontLayout.addWidget(table)
        self.setLayout(self.horizontLayout)
        # printf('Unit1')

        self.lst_data_val = []
        # return self.page

    def is_valid_email(self,data):
        # return re.match('^[0-9]*[.][0-9]+$', data) is not None
        return re.match('^-?\d+\.?\d*$', data) is not None

    def changedValue(self, value):
        # printff(value.data)
        if self.readData_flag ==0:
            item = self.lst_model[self.index_data_tab].item(value.row(), value.column())
            # if not value.text().isalpha() and '.' in self.checkValue and '.' in value.text():
            # printff(self.checkValue,value.text())
            if (not '.' in self.checkValue) and (not '.' in value.text()) and \
                    self.is_valid_email(value.text()) and self.is_valid_email(self.checkValue):
                # printff('Data_int', value.text(), value.row())
                self.checkValue = value.text()
                item.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 9)))
            elif '.' in self.checkValue and '.' in value.text() and \
                self.is_valid_email(self.checkValue) and self.is_valid_email(value.text()):
                # printff('Data_float', value.text(), value.row())
                self.checkValue = value.text()
                item.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 9)))
            else:
                # printff('CHANGE',value.row(),value.column(),self.checkValue)
                item.setChild(value.row(),value.column(), item.setText(self.checkValue))


    def selectRow1(self, data):
        self.checkValue = data.data()
        self.curr_row = data.row()
        printf('SELECT', data.row(), data.column(), data.data())


    # def keyPressEvent(self, e):
    def on_key(self, e):
        if e == PyQt5.Qt.Qt.Key_Up:
            if self.curr_row!=0:
                self.curr_row-=1
                item = self.lst_model[self.index_data_tab].item(self.curr_row, 2)
                self.checkValue = item.text()
        if e == PyQt5.Qt.Qt.Key_Down:
            if self.curr_row<self.cnt_elem-1:
                self.curr_row+=1
                item = self.lst_model[self.index_data_tab].item(self.curr_row, 2)
                self.checkValue = item.text()

    def selectDataTab(self,index):
        self.index_data_tab = index

    def enteredValue(self,value):
        printf('ENTERED',value.data())

    def pressedValue(self,value):
        printf('PRESSED',value.data())

    def activatedValue(self,value):
        printf('ACTIVATED',value.data())

    def readData(self,data_dict,data,count_read):
        self.readData_flag =1
        # self.lst_model[0].itemChanged.disconnect()
        count =0;count1 =0;num=0
        cnt_row = self.lst_model[0].rowCount()
        preset_indx = 9
        calibr_indx = 2
        self.count_read = count_read
        # if self.count_read >=4:
        #     preset_indx+=self.count_read
        #     calibr_indx+=1
        #     printf(preset_indx)
        # # for i in self.data_tab.count():
        for i in data_dict[data].items():
            item = self.lst_model[num].item(count, 2)
            item.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            if data =='preset':
                #test
                self.checkValue = str(i[1][5])
                # self.checkValue = str(i[1][preset_indx])
                #test
                item.setChild(count, 2, item.setText(str(i[1][5])))
                # item.setChild(count, 2, item.setText(str(i[1][preset_indx])))
            else:
                self.checkValue = str(i[1][calibr_indx])
                item.setChild(count, 2, item.setText(str(i[1][calibr_indx])))
            count+=1
            if count == cnt_row:
                count =0
                count1+=1
                num+=1
                if count1 == self.data_tab.count():
                    self.readData_flag = 0
                    return 0
                    # printff(num)
                    # item = self.lst_model[num].item(count, 2)
                # else: printff(data_dict); return 0
        self.readData_flag = 0
        printf(data_dict['preset'].items())

        printf(data_dict)
    def writeData(self,data_dict,data):
        printf('WriteData')
        count =0
        lst_data_dict_keys = list(data_dict[data].keys())
        for i in range(0,self.data_tab.count()):
            for j in range(0, self.lst_model[i].rowCount()):
                item = self.lst_model[i].item(j, 2)
                # item1.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                if data =='preset':
                    data_dict[data].get(lst_data_dict_keys[count])[9] = item.text()
                else:
                    data_dict[data].get(lst_data_dict_keys[count])[2] = item.text()
                count+=1
        # printf(data_dict[data].items())
        printf(data_dict)
        return data_dict

    def saveData(self,obj_cal,data,name_block,name_product,list_nmb):
        step = 0
        step += 10
        self.cal_signal.emit(step)
        printf('SaveData')

        import csv
        import os

        folder = 'csv,pdf,bin'
        os.makedirs(folder, exist_ok=True)
        lst_data = []

        name_block_rus = '0'
        name_product_rus = '0'
        name_drawing = '0'
        if name_product == 'SES200M':
            name_product_rus = 'СЭС-200М'
            if name_block == 'BU_400':
                name_block_rus = 'БУ400'; name_drawing = "ТАКИ.466539.022"
            elif name_block == 'BU_50':
                name_block_rus = 'БУ50'; name_drawing = "ТАКИ.466539.023"
            elif name_block == 'BU_SES':
                name_block_rus = 'БУСЭС'; name_drawing = "ТАКИ.466539.024"
        elif name_product == "SEP30M":
            name_product_rus = 'СЭП-30М'
            if name_block == 'BU_400':
                name_block_rus = 'БУ400'; name_drawing = "ТАКИ.466539.021"
            elif name_block == 'BU_SEP':
                name_block_rus = 'БУСЭП'; name_drawing = "ТАКИ.466539.020"

        name_block = name_block.lower()

        output_file = name_product_rus+'_'+list_nmb[0]+'_'+name_block_rus+'_' +list_nmb[1]+'_'+ name_drawing[:4]+'_'+name_drawing[-3:] +'_'+data

        step += 10
        self.cal_signal.emit(step)

        data_dict_copy = obj_cal.data_dict.copy()
        count =0
        lst_data_dict_keys = list(data_dict_copy[data].keys())
        printf(lst_data_dict_keys)
        with open(f'./{folder}/{output_file}.bin','wb') as f:
            printf(obj_cal.header_data_dict[data])
            for i in obj_cal.header_data_dict[data][0:]:
                printf('i',i)
                f.write(i)
            printf(data)
            if data == 'filter':
                printf(obj_cal.data_dict[data])
                for i in obj_cal.data_dict[data]:
                    printf()
                    f.write(struct.pack('I', int(obj_cal.data_dict[data][i][0])))
                    printf()
                    f.write(struct.pack('I', int(obj_cal.data_dict[data][i][1])))
            else:
                for i in range(0,self.data_tab.count()):
                    for j in range(0, self.lst_model[i].rowCount()):
                        designation = self.lst_model[i].item(j, 0)
                        name = self.lst_model[i].item(j, 1)
                        item = self.lst_model[i].item(j, 2)
                        #для csv
                        local_lst_data = [designation.text(), name.text(), item.text()]
                        lst_data.append(local_lst_data)
                        # item1.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        dt_dict = data_dict_copy[data].get(lst_data_dict_keys[count])
                        printf(dt_dict,item.text())
                        if data == 'preset':
                            if data_dict_copy[data].get(lst_data_dict_keys[count])[1] == 'float':
                                f.write(struct.pack('f', float(dt_dict[3])))
                                f.write(struct.pack('f', float(dt_dict[4])))
                                f.write(struct.pack('f', float(item.text())))
                                f.write(struct.pack('f', float(dt_dict[6])))
                            else:
                                if data_dict_copy[data].get(lst_data_dict_keys[count])[2] == 'с':
                                    dt_dict[3] = str(int(float(dt_dict[3])))
                                    f.write(struct.pack('i', int(dt_dict[3])))
                                    dt_dict[4] = str(int(float(dt_dict[4])))
                                    f.write(struct.pack('i', int(dt_dict[4])))
                                    # dt_item    = str(int(float(item.text())* 1000))
                                    dt_item    = str(int(float(item.text())))
                                    f.write(struct.pack('i', int(dt_item)))
                                    dt_dict[6] = str(int(float(dt_dict[6])))
                                    f.write(struct.pack('i', int(dt_dict[6])))
                                    printf(dt_dict[3],dt_dict[4],dt_item,dt_dict[6])
                                else:
                                    f.write(struct.pack('i', int(dt_dict[3])))
                                    f.write(struct.pack('i', int(dt_dict[4])))
                                    f.write(struct.pack('i', int(item.text())))
                                    f.write(struct.pack('i', int(dt_dict[6])))
                        else:
                            f.write(struct.pack('f', float(item.text())))
                        count+=1
                step += 10
                self.cal_signal.emit(step)
                #Запись в csv
                head_myData = [["Обозначение","Наименование","Значение"]]
                myFile = open(f'./{folder}/{output_file}.csv', 'w', encoding='utf-32', newline='')
                with myFile:
                    writer = csv.writer(myFile, delimiter='\t')
                    writer.writerows(head_myData)
                    writer.writerows(lst_data)

                step += 10
                self.cal_signal.emit(step)

                # Запись в pdf рабочая версия
                # if data!='filter':
                #     from reportlab.lib import colors
                #     from reportlab.lib.pagesizes import letter, inch, A4
                #     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
                #     from reportlab.pdfbase import pdfmetrics
                #     from reportlab.pdfbase.ttfonts import TTFont
                #     from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
                #     from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
                #
                #     lst_data.insert(0, head_myData[0])
                #     doc = SimpleDocTemplate(f'./{folder}/{output_file}.pdf', pagesize=letter)
                #
                #     # styles = getSampleStyleSheet()
                #     story = []
                #
                #     elements = []
                #
                #     pdfmetrics.registerFont(TTFont('TimesNewRomanCyrillic', 'timesnrcyrmt.ttf'))
                #     pdfmetrics.registerFont(TTFont('TimesNewRomanCyrillicBold', 'timesnrcyrmt_bold.ttf'))
                #     style_cyrillic_bold = ParagraphStyle(
                #         name='CyrillicStyle',
                #         fontName='TimesNewRomanCyrillicBold',
                #         fontSize=12,
                #         leading=11,
                #         alignment=TA_CENTER
                #     )
                #     style_cyrillic_left = ParagraphStyle(
                #         name='CyrillicStyle',
                #         fontName='TimesNewRomanCyrillic',
                #         fontSize=11,
                #         leading=11
                #     )
                #     style_cyrillic = ParagraphStyle(
                #         name='CyrillicStyle',
                #         fontName='TimesNewRomanCyrillic',
                #         fontSize=11,
                #         leading=11,
                #         alignment=TA_CENTER
                #     )
                #     style_cyrillic_head = ParagraphStyle(
                #         name='Normal',
                #         fontName='TimesNewRomanCyrillic',
                #         fontSize=12,
                #         leading=11,
                #         alignment=TA_LEFT,
                #         spaceAfter=-12,
                #         spaceBefore=10
                #         # parent=styles['Normal']
                #     )
                #     style_cyrillic_head_bold = ParagraphStyle(
                #         name='Normal',
                #         fontName='TimesNewRomanCyrillicBold',
                #         fontSize=12,
                #         leading=11,
                #         alignment=TA_RIGHT,
                #         spaceAfter=22,
                #         spaceBefore=10
                #         # parent=styles['Normal']
                #     )
                #     # 2. Создаем текст заголовка
                #     product_text = 'Изделие:'
                #     product_paragraph = Paragraph(product_text, style_cyrillic_head_bold)
                #     name_product_text = name_product_rus
                #     name_product_paragraph = Paragraph(name_product_text, style_cyrillic_head)
                #     product_nmb_text = 'зав.№:'
                #     product_nmb_paragraph = Paragraph(product_nmb_text, style_cyrillic_head_bold)
                #     product_nmb_val_text = list_nmb[0]
                #     product_nmb_val_paragraph = Paragraph(product_nmb_val_text, style_cyrillic_head)
                #
                #     cb_text = 'Блок:'
                #     cb_paragraph = Paragraph(cb_text, style_cyrillic_head_bold)
                #     name_cb_text = name_block_rus + ', ' + name_drawing
                #     name_cb_paragraph = Paragraph(name_cb_text, style_cyrillic_head)
                #     cb_nmb_text = 'зав.№:'
                #     cb_nmb_paragraph = Paragraph(cb_nmb_text, style_cyrillic_head_bold)
                #     cb_nmb_val_text = list_nmb[1]
                #     name_cb_val_paragraph = Paragraph(cb_nmb_val_text, style_cyrillic_head)
                #
                #     table_paragraph = [
                #         [product_paragraph, name_product_paragraph, product_nmb_paragraph, product_nmb_val_paragraph], []]
                #
                #     table_data_paragraph = Table(table_paragraph, colWidths=[0.9 * 72, 1.1 * 72, 0.7 * 72, 0.8 * 72])
                #     # table_data_paragraph = Table(table_paragraph)
                #     table_data_paragraph.setStyle(TableStyle([
                #         # ('INNERGRID', (0, 0), (2, -1), 0.25, colors.black),
                #         ('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.black),
                #         # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                #     ]))
                #
                #     table_paragraph2 = [
                #         [cb_paragraph, name_cb_paragraph, cb_nmb_paragraph, name_cb_val_paragraph], [], []]
                #     table_data_paragraph2 = Table(table_paragraph2, colWidths=[0.7 * 72, 2.2 * 72, 0.7 * 72, 0.8 * 72])
                #     # table_data_paragraph2 = Table(table_paragraph2)
                #
                #     table_data_paragraph2.setStyle(TableStyle([
                #         # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                #         ('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.black),
                #         # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                #     ]))
                #     table_data = []
                #     table_row = []
                #     cnt2 = 0
                #     for row in lst_data:
                #         cnt = 0
                #         for text in row:
                #             if cnt2 < 3:
                #                 table_row.append(Paragraph(text, style_cyrillic_bold))
                #             elif cnt == 1 and cnt2 != 1:
                #                 table_row.append(Paragraph(text, style_cyrillic_left))
                #             else:
                #                 table_row.append(Paragraph(text, style_cyrillic))
                #             cnt += 1
                #             cnt2 += 1
                #         table_data.append(table_row)
                #         table_row = []
                #     # t=Table(table_data,5*[0.5*inch], 4*[0.3*inch])
                #     # t = Table(table_data)
                #     if data == 'preset':
                #         width_0 = 1.4 * 72
                #         width_1 = 5 * 72
                #     else:
                #         width_0 = 2.4 * 72
                #         width_1 = 4 * 72
                #     t = Table(table_data, colWidths=[width_0, width_1, 1.1 * 72], repeatRows=1)
                #     t.setStyle(TableStyle([
                #         #                        ('ALIGN', (1, 1), (-1, -2), 'RIGHT'),
                #         #                        ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                #         #                        ('VALIGN', (0, 0), (0, -1), 'TOP'),
                #         #                        ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                #         #                        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                #         #                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                #         #                        ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                #         ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                #         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                #         ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                #     ]))
                #
                #     elements.append(t)
                #     # write the document to disk
                #     story.append(table_data_paragraph)
                #     story.append(table_data_paragraph2)
                #     story.append(t)
                #     doc.build(story)
                step += 10
                self.cal_signal.emit(step)
                step = 100
                self.cal_signal.emit(step)

                # # Запись в docx
                # from docx import Document
                # from docx.enum.text import WD_ALIGN_PARAGRAPH
                # from docx.shared import Pt,Inches
                # from docx.enum.table import WD_TABLE_ALIGNMENT
                #
                # # создание пустого документа
                # doc = Document()
                # # добавление параграфа
                # paragraph1 = doc.add_paragraph()
                # paragraph1.add_run('Изделие: ').bold = True
                # paragraph1.add_run(f'{name_product_rus}, ')
                # paragraph1.add_run('зав.№: ').bold = True
                # paragraph1.add_run(f'{list_nmb[0]}')
                # paragraph1.alignment = WD_ALIGN_PARAGRAPH.CENTER
                # paragraph2 = doc.add_paragraph()
                # paragraph2.add_run('Блок: ').bold = True
                # paragraph2.add_run(f'{name_block_rus}, {name_drawing}, ')
                # paragraph2.add_run('зав.№: ').bold = True
                # paragraph2.add_run(f'{list_nmb[1]}')
                # paragraph2.alignment = WD_ALIGN_PARAGRAPH.CENTER
                #
                # # добавляем таблицу с одной строкой
                # # для заполнения названий колонок
                # table = doc.add_table(1, len(lst_data[0]))
                # # определяем стиль таблицы
                # # table.style = 'Light Shading Accent 1'
                # table.style = 'Table Grid'
                # table.alignment = WD_TABLE_ALIGNMENT.CENTER
                #
                # libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
                #
                # # Устанавливаем размер второго столбца
                # if not os.path.exists(libreoffice_path):
                #     libreoffice_path = r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
                #     if not os.path.exists(libreoffice_path):
                #         if data =='preset':
                #             table.columns[0].width = Inches(0.5)
                #             table.columns[1].width = Inches(20)
                #         else:
                #             table.columns[0].width = Inches(1)
                #             table.columns[1].width = Inches(20)
                #         table.columns[2].width = Inches(0.5)
                #     else:
                #         if data =='preset':
                #             table.columns[0].width = Inches(1.5)
                #             table.columns[1].width = Inches(5)
                #         else:
                #             table.columns[0].width = Inches(2.4)
                #             table.columns[1].width = Inches(4.2)
                #         table.columns[2].width = Inches(1)
                # else:
                #     if data == 'preset':
                #         table.columns[0].width = Inches(1.5)
                #         table.columns[1].width = Inches(5)
                #     else:
                #         table.columns[0].width = Inches(2.4)
                #         table.columns[1].width = Inches(4.2)
                #     table.columns[2].width = Inches(1)
                # # Получаем строку с колонками из добавленной таблицы
                # head_cells = table.rows[0].cells
                # # добавляем названия колонок
                # for i, item in enumerate(head_myData[0]):
                #     p = head_cells[i].paragraphs[0]
                #     # p.runs[0].font.name = 'Times New Roman'
                #     # название колонки
                #     p.add_run(item).bold = True
                #     # выравниваем посередине
                #     p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                # for i in table.rows:
                #     for cell in i.cells:
                #         cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
                #         cell.paragraphs[0].runs[0].font.size = Pt(12)
                # # добавляем данные к существующей таблице
                # for row in lst_data:
                #     # добавляем строку с ячейками к объекту таблицы
                #     cells = table.add_row().cells
                #     for i, item in enumerate(row):
                #         # вставляем данные в ячейки
                #         cells[i].text = str(item)
                #         # если последняя ячейка
                #         cells[i].paragraphs[0].runs[0].font.name = 'Times New Roman'
                #         cells[i].paragraphs[0].runs[0].font.size = Pt(12)
                #         if i ==0 or i ==2:
                #             cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                #
                # doc.save(f'./{folder}/{output_file}.docx')
                #
                # step += 10
                # self.cal_signal.emit(step)
                # # Для LibreOffice на Windows
                # import subprocess
                # docx_path = f"./{folder}/{output_file}.docx"
                # output_dir = f"./{folder}/{output_file}.pdf"
                # if not os.path.exists(libreoffice_path):
                #     libreoffice_path = r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
                #     if not os.path.exists(libreoffice_path):
                #         # Конвертация в pdf 2-й способ нужен установленный Word
                #         import sys
                #         import comtypes.client
                #         dirs = sys.executable
                #         wdFormatPDF = 17
                #         out_file = self.trans_path(dirs, output_file, folder)
                #         # out_file = 'D:\\repo\\calibrator\\prj2\csv,docx,pdf\\'+output_file
                #         # for subdir, dirs, files in os.walk(input_dir):
                #         #     printf(subdir,dirs,files)
                #         #     for file in files:
                #         #         in_file = os.path.join(subdir, file)
                #         # output_file = file.split('.')[0]
                #         # out_file = output_dir + output_file +'.pdf'
                #         word = comtypes.client.CreateObject('Word.Application')
                #         doc = word.Documents.Open(out_file + '.docx')
                #         doc.SaveAs(out_file + '.pdf', FileFormat=wdFormatPDF)
                #         doc.Close()
                #         word.Quit()
                #         # raise FileNotFoundError(f"LibreOffice executable not found at: {libreoffice_path}")
                #
                # # Создает директорию
                # # if not os.path.exists(output_dir):
                # #     os.makedirs(output_dir)
                # command = [
                #     libreoffice_path,
                #     "--headless",  # Run LibreOffice without a graphical interface
                #     "--convert-to", "pdf",
                #     "--outdir", folder,
                #     docx_path
                # ]
                #
                # try:
                #     subprocess.run(command, check=True, capture_output=True, text=True)
                #     print(f"Successfully converted '{docx_path}' to PDF in '{output_dir}'.")
                # except subprocess.CalledProcessError as e:
                #     print(f"Error during conversion: {e}")
                #     print(f"Stdout: {e.stdout}")
                #     print(f"Stderr: {e.stderr}")
                # except FileNotFoundError:
                #     print(f"Error: LibreOffice executable not found at {libreoffice_path}.")
                #
                # step = 100
                # self.cal_signal.emit(step)
                # # Конвертация в pdf
                # printf("-" * 50 + "\nКонвертация .docx в .pdf:\n" + "-" * 50)
                # ok =True
                # try:
                #     import docx2pdf
                # except Exception as e:
                #     printf(f"Ошибка импорта модуля! Подробнее:\n{e}"); ok = False
                # if ok:
                #     input_file = f"./{folder}/{output_file}.docx"
                #     output_file = f"./{folder}/{output_file}.pdf"
                #     if not os.path.exists(input_file):
                #         printf(f"Файл {input_file} не найден! Выполнение конвертации невозможно!")
                #     else:
                #         docx2pdf.convert(input_file, output_file)

        printf(data_dict_copy)
        return data_dict_copy
    def saveDataval(self):

        source = ''
        head_myData = [['Источник', "Обозначение параметра", "Наименование параметра", "Значение"]]

        for i in range(0, self.data_tab.count()):
            for j in range(0, self.lst_model[i].rowCount()):
                designation = self.lst_model[i].item(j, 0)
                name = self.lst_model[i].item(j, 1)
                value = self.lst_model[i].item(j, 2)
                if designation.text()[0:3] in 'FC1' or designation.text()[0:3] in 'FC2':
                    source = 'ПЧ-100'
                elif designation.text()[0:2] in 'N_':
                    source = 'Ввод 1'
                elif designation.text()[0:2] in 'N2':
                    source = 'Ввод 2'
                elif designation.text()[0:2] in 'EA':
                    source = 'ЭА'
                elif designation.text()[0:2] in 'EN':
                    source = 'Электронагреватель'
                elif designation.text()[0:3] in 'AIR':
                    source = 'Термодатчик'
                elif designation.text()[0:6] in 'U_AB_S':
                    source = 'Аккумуляторная батарея СТ'
                elif designation.text()[0:6] in 'U_AB_O' or designation.text()[0:4] in 'U_OP':
                    source = 'Аккумуляторная батарея ОП'
                elif designation.text()[0:7] in 'LEVEL_F':
                    source = 'Датчик уровня топлива в баке № 1'
                elif designation.text()[0:7] in 'LEVEL_E':
                    source = 'Датчик уровня топлива в баке № 2'
                elif designation.text()[0:4] in 'SPCH':
                    source = 'СПЧ'
                elif designation.text()[0:3] in 'B_I':
                    source = 'Общая шина'

                local_lst_data = [source, designation.text(), name.text(), value.text()]
                self.lst_data_val.append(local_lst_data)
        self.lst_data_val.insert(0, head_myData[0])

    def saveDatapdf(self,name_product,unit_obj,list_nmb):

        import os
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, inch, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
        from reportlab.lib.enums import TA_CENTER, TA_LEFT,TA_RIGHT

        folder = 'csv,pdf'
        os.makedirs(folder, exist_ok=True)
        p_bu1 =0
        p_bu2=0
        p_bu3 =0
        story = []
        name_product_rus = '0'

        style_cyrillic_bold = ParagraphStyle(
            name='CyrillicStyle',
            fontName='TimesNewRomanCyrillicBold',
            fontSize=13,
            leading=15,
            spaceAfter=6,
            alignment=TA_CENTER
        )
        style_cyrillic_bold_right = ParagraphStyle(
            name='CyrillicStyle',
            fontName='TimesNewRomanCyrillicBold',
            fontSize=13,
            leading=15,
            spaceAfter=6,
            leftIndent=10,
            # rightIndent=10
        )
        style_cyrillic_bold_right_space = ParagraphStyle(
            name='CyrillicStyle',
            fontName='TimesNewRomanCyrillicBold',
            fontSize=13,
            leading=15,
            spaceAfter=6,
            spaceBefore=25,
            leftIndent=7,
            # rightIndent=10
        )
        style_cyrillic_left = ParagraphStyle(
            name='CyrillicStyle',
            fontName='TimesNewRomanCyrillic',
            fontSize=11,
            leading=11
        )
        style_cyrillic = ParagraphStyle(
            name='CyrillicStyle',
            fontName='TimesNewRomanCyrillic',
            fontSize=11,
            leading=11,
            alignment=TA_CENTER
        )
        p1 = Paragraph("Приложение Б", style_cyrillic_bold)
        p2 = Paragraph("Калибровочные коэффициенты", style_cyrillic_bold)
        if name_product == 'SES200M':
            name_product_rus = 'СЭС-200М'
            p_bu1 = Paragraph("Б.1 Калибровочные коэффициенты блока управления 400 Гц ТАКИ.466539.022",
                              style_cyrillic_bold_right)
            p_bu2 = Paragraph("Б.2 Калибровочные коэффициенты блока управления 50 Гц ТАКИ.466539.023",
                              style_cyrillic_bold_right_space)
            p_bu3 = Paragraph("Б.3 Калибровочные коэффициенты блока управления СЭС ТАКИ.466539.024",
                              style_cyrillic_bold_right_space)
        elif name_product == "SEP30M":
            name_product_rus = 'СЭП-30М'
            p_bu1 = Paragraph("20.1 Калибровочные коэффициенты блока управления СЭП ТАКИ.466539.020",
                              style_cyrillic_bold_right)
            p_bu2 = Paragraph("20.2 Калибровочные коэффициенты блока управления 400 Гц ТАКИ.468127.155",
                              style_cyrillic_bold_right_space)

        output_file = name_product_rus + '_'+list_nmb[0]+ '_calibr'
        doc = SimpleDocTemplate(f'./{folder}/{output_file}.pdf', pagesize=letter,topMargin=0.4*inch,
                                leftMargin=0.8*inch,bottomMargin=0.8*inch)
        pdfmetrics.registerFont(TTFont('TimesNewRomanCyrillic', 'timesnrcyrmt.ttf'))
        pdfmetrics.registerFont(TTFont('TimesNewRomanCyrillicBold', 'timesnrcyrmt_bold.ttf'))

        for i in range(0,len(unit_obj)):
            table_data = []
            table_row = []
            cnt2 = 0
            for row in unit_obj[i].lst_data_val:
                cnt = 0
                for text in row:
                    if cnt2 < 3:
                        table_row.append(Paragraph(text, style_cyrillic))
                    elif cnt == 1 and cnt2 != 1 or cnt == 2 and cnt2 != 2:
                        table_row.append(Paragraph(text, style_cyrillic_left))
                    else:
                        table_row.append(Paragraph(text, style_cyrillic))
                    cnt += 1
                    cnt2 += 1
                table_data.append(table_row)
                table_row = []
            t = Table(table_data, colWidths=[1.1 * 72, 2.3*72, 2.5*72, 1.3 * 72], repeatRows=1,hAlign="LEFT")

            if i ==0:
                if name_product == "SES200M":
                    t.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('SPAN', (0, 1), (0, 2)),('SPAN', (0, 3), (0, 4)),('SPAN', (0, 5), (0, 6)),
                    ('SPAN', (0, 7), (0, 33)),('SPAN', (0, 34), (0, 50)),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),]))
                elif name_product == "SEP30M":
                    t.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('SPAN', (0, 1), (0, 6)), ('SPAN', (0, 7), (0, 18)), ('SPAN', (0, 19), (0, 30)),
                        ('SPAN', (0, 31), (0, 36)), ('SPAN', (0, 37), (0, 48)), ('SPAN', (0, 49), (0, 54)),
                        ('SPAN', (0, 55), (0, 56)), ('SPAN', (0, 57), (0, 58)), ('SPAN', (0, 59), (0, 60)),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
                story.append(p1)
                story.append(p2)
                story.append(p_bu1)
            elif i ==1:
                if name_product == "SES200M":
                    t.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('SPAN', (0, 1), (0, 19)),('SPAN', (0, 20), (0, 34)),('SPAN', (0, 35), (0, 58)),
                        ('SPAN', (0, 59), (0, 68)),('SPAN', (0, 69), (0, 97)),('SPAN', (0, 98), (0, 108)),
                        ('SPAN', (0, 109), (0, 114)), ('SPAN', (0, 115), (0, 126)),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),]))
                elif name_product == "SEP30M":
                    t.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('SPAN', (0, 1), (0, 9)), ('SPAN', (0, 10), (0, 18)),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
                story.append(p_bu2)
            else:
                t.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('SPAN', (0, 1), (0, 2)),('SPAN', (0, 3), (0, 4)),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),]))
                story.append(p_bu3)

            story.append(t)

        doc.build(story)

    #test записи в csv
    def saveDatatest(self,data,name_block,name_product,list_nmb):
        # count_elem += 1
        # if count_elem == proc_elem:
        step = 0
        step += 10
        self.cal_signal.emit(step)

        printf('saveDatatest')
        import csv
        import os
        folder = 'csv,pdf'
        os.makedirs(folder, exist_ok=True)

        name_block_rus = '0'
        name_product_rus = '0'
        name_drawing = '0'
        if name_product == 'SES200M':
            name_product_rus = 'СЭС-200М'
            if name_block == 'BU_400':
                name_block_rus = 'БУ400'; name_drawing = "ТАКИ.466539.022"
            elif name_block == 'BU_50':
                name_block_rus = 'БУ50'; name_drawing = "ТАКИ.466539.023"
            elif name_block == 'BU_SES':
                name_block_rus = 'БУСЭС'; name_drawing = "ТАКИ.466539.024"
        elif name_product == "SEP30M":
            name_product_rus = 'СЭП-30М'
            if name_block == 'BU_400':
                name_block_rus = 'БУ400'; name_drawing = "ТАКИ.466539.021"
            elif name_block == 'BU_SEP':
                name_block_rus = 'БУСЭП'; name_drawing = "ТАКИ.466539.020"

        output_file = name_product_rus+'_'+list_nmb[0]+'_'+name_block_rus+'_' +list_nmb[1]+'_'+ name_drawing[:4]+'_'+name_drawing[-3:] +'_'+data

        step += 10
        self.cal_signal.emit(step)

        lst_data = []
        source = ''
        #Запись в csv
        head_myData = [['Источник',"Обозначение параметра","Наименование параметра","Значение"]]
        for i in range(0, self.data_tab.count()):
            for j in range(0, self.lst_model[i].rowCount()):
                designation = self.lst_model[i].item(j, 0)
                name = self.lst_model[i].item(j, 1)
                value = self.lst_model[i].item(j, 2)
                if designation.text()[0:3] in 'FC1' or designation.text()[0:3] in 'FC2':
                   source = 'ПЧ-100'
                elif designation.text()[0:2] in 'N_':
                    source = 'Ввод 1'
                elif designation.text()[0:2] in 'N2':
                    source = 'Ввод 2'
                elif designation.text()[0:2] in 'EA':
                    source = 'ЭА'
                elif designation.text()[0:2] in 'EN':
                    source = 'Электронагреватель'
                elif designation.text()[0:3] in 'AIR':
                    source = 'Термодатчик'
                elif designation.text()[0:6] in 'U_AB_S':
                    source = 'Аккумуляторная батарея СТ'
                elif designation.text()[0:6] in 'U_AB_O':
                    source = 'Аккумуляторная батарея ОП'
                elif designation.text()[0:7] in 'LEVEL_F':
                    source = 'Датчик уровня топлива в баке № 1'
                elif designation.text()[0:7] in 'LEVEL_E':
                    source = 'Датчик уровня топлива в баке № 2'
                local_lst_data =[source,designation.text(),name.text(),value.text()]
                lst_data.append(local_lst_data)
        myFile = open(f'./{folder}/{output_file}.csv', 'w', encoding='utf-32', newline='')
        with myFile:
            writer = csv.writer(myFile, delimiter='\t')
            writer.writerows(head_myData)
            writer.writerows(lst_data)
            # writer.writerows(params_xml_list)

        step += 10
        self.cal_signal.emit(step)
        printf(lst_data)
        # with open('read_data.txt', 'w') as self.file_open:
        # self.file_open.write('hi1')

        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, inch, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
        from reportlab.lib.enums import TA_CENTER, TA_LEFT,TA_RIGHT

        lst_data.insert(0,head_myData[0])
        doc = SimpleDocTemplate(f'./{folder}/{output_file}.pdf', pagesize=letter,topMargin=0.1*inch)
        # styles = getSampleStyleSheet()
        story = []
        elements = []

        pdfmetrics.registerFont(TTFont('TimesNewRomanCyrillic', 'timesnrcyrmt.ttf'))
        pdfmetrics.registerFont(TTFont('TimesNewRomanCyrillicBold', 'timesnrcyrmt_bold.ttf'))
        style_cyrillic_bold = ParagraphStyle(
            name='CyrillicStyle',
            fontName='TimesNewRomanCyrillicBold',
            fontSize=12,
            leading=15,
            spaceAfter=6,
            # spaceBefore=10,
            alignment=TA_CENTER
        )
        style_cyrillic_left = ParagraphStyle(
            name='CyrillicStyle',
            fontName='TimesNewRomanCyrillic',
            fontSize=11,
            leading=11
        )
        style_cyrillic = ParagraphStyle(
            name='CyrillicStyle',
            fontName='TimesNewRomanCyrillic',
            fontSize=11,
            leading=11,
            alignment=TA_CENTER
        )

        p1 = Paragraph("Приложение Б", style_cyrillic_bold)
        p2 = Paragraph("Калибровочные коэффициенты", style_cyrillic_bold)
        if name_block =='BU_400':
            p3 = Paragraph("Б.1 Калибровочные коэффициенты блока управления 400 Гц ТАКИ.466539.022", style_cyrillic_bold)
        elif name_block =='BU_50':
            p3 = Paragraph("Б.2 Калибровочные коэффициенты блока управления 50 Гц ТАКИ.466539.023", style_cyrillic_bold)
        else:
            p3 = Paragraph("Б.3 Калибровочные коэффициенты блока управления 50 Гц ТАКИ.466539.024", style_cyrillic_bold)

        table_data = []
        table_row = []
        cnt2 = 0
        for row in lst_data:
            cnt =0
            for text in row:
                if cnt2<3:
                    table_row.append(Paragraph(text, style_cyrillic))
                elif cnt ==1 and cnt2 !=1 or cnt ==2 and cnt2 !=2:
                    table_row.append(Paragraph(text, style_cyrillic_left))
                else:
                    table_row.append(Paragraph(text, style_cyrillic))
                cnt+=1
                cnt2+=1
            table_data.append(table_row)
            table_row = []
        width_0 = 2.3*72
        width_1 = 2.5 * 72
        t = Table(table_data,colWidths=[1.1*72,width_0, width_1, 1.1*72],repeatRows=1)
        t.setStyle(TableStyle([
        #                        ('ALIGN', (1, 1), (-1, -2), 'RIGHT'),
        #                        ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
        #                        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        #                        ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
        #                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
        #                        ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Горизонтальное выравнивание
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Вертикальное выравнивание
                               # ('SPAN', (0, 1), (0, 2)),
                               # ('SPAN', (0, 3), (0, 4)),
                               # ('SPAN', (0, 5), (0, 6)),
                               # ('SPAN', (0, 7), (0, 30)),
                               # ('SPAN', (0, 31), (0, 50)),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ]))
        elements.append(t)
        story.append(p1)
        story.append(p2)
        story.append(p3)
        story.append(t)
        doc.build(story)

        step += 10
        self.cal_signal.emit(step)
        step = 100
        self.cal_signal.emit(step)

        # Запись в docx
        # from docx import Document
        # from docx.enum.text import WD_ALIGN_PARAGRAPH
        # from docx.shared import Pt,Inches
        # from docx.enum.table import WD_TABLE_ALIGNMENT
        #
        # libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
        # # создание пустого документа
        # doc = Document()
        #
        # # добавление параграфа
        # paragraph1 = doc.add_paragraph()
        # paragraph1.add_run('Изделие: ').bold = True
        # paragraph1.add_run(f'{name_product_rus}, ')
        # paragraph1.add_run('зав.№: ').bold = True
        # paragraph1.add_run(f'{list_nmb[0]}')
        # paragraph1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # paragraph2 = doc.add_paragraph()
        # paragraph2.add_run('Блок: ').bold = True
        # paragraph2.add_run(f'{name_block_rus}, {name_drawing}, ')
        # paragraph2.add_run('зав.№: ').bold = True
        # paragraph2.add_run(f'{list_nmb[1]}')
        # paragraph2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # # добавляем таблицу с одной строкой
        # # для заполнения названий колонок
        # table = doc.add_table(1, len(lst_data[0]))
        # # определяем стиль таблицы
        # # table.style = 'Light Shading Accent 1'
        # table.style = 'Table Grid'
        # table.alignment = WD_TABLE_ALIGNMENT.CENTER
        # # Устанавливаем размер второго столбца
        # if not os.path.exists(libreoffice_path):
        #     libreoffice_path = r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        #     if not os.path.exists(libreoffice_path):
        #         if data =='preset':
        #             table.columns[0].width = Inches(0.5)
        #             table.columns[1].width = Inches(20)
        #         else:
        #             table.columns[0].width = Inches(1)
        #             table.columns[1].width = Inches(20)
        #         table.columns[2].width = Inches(0.5)
        #     else:
        #         if data =='preset':
        #             table.columns[0].width = Inches(1.5)
        #             table.columns[1].width = Inches(5)
        #         else:
        #             table.columns[0].width = Inches(2.4)
        #             table.columns[1].width = Inches(4.2)
        #         table.columns[2].width = Inches(1)
        # else:
        #     if data == 'preset':
        #         table.columns[0].width = Inches(1.5)
        #         table.columns[1].width = Inches(5)
        #     else:
        #         table.columns[0].width = Inches(2.4)
        #         table.columns[1].width = Inches(4.2)
        #     table.columns[2].width = Inches(1)
        # # Получаем строку с колонками из добавленной таблицы
        # head_cells = table.rows[0].cells
        # # добавляем названия колонок
        # for i, item in enumerate(head_myData[0]):
        #     p = head_cells[i].paragraphs[0]
        #     # p.runs[0].font.name = 'Times New Roman'
        #     # название колонки
        #     p.add_run(item).bold = True
        #     # выравниваем посередине
        #     p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # for i in table.rows:
        #     for cell in i.cells:
        #         cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        #         cell.paragraphs[0].runs[0].font.size = Pt(12)
        # # добавляем данные к существующей таблице
        # for row in lst_data:
        #     # добавляем строку с ячейками к объекту таблицы
        #     cells = table.add_row().cells
        #     for i, item in enumerate(row):
        #         # вставляем данные в ячейки
        #         cells[i].text = str(item)
        #         # если последняя ячейка
        #         cells[i].paragraphs[0].runs[0].font.name = 'Times New Roman'
        #         cells[i].paragraphs[0].runs[0].font.size = Pt(12)
        #         if i ==0 or i ==2:
        #             cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        #
        # doc.save(f'./{folder}/{output_file}.docx')
        # paragraph3 = doc.add_paragraph()
        # doc.save('test.docx')

        # self.file_open.write('hi2')

        # Конвертация в pdf 1-й способ нужен установленный Word
        # printf("-" * 50 + "\nКонвертация .docx в .pdf:\n" + "-" * 50)
        # ok =True
        # import docx2pdf
        # self.file_open.write('hi3')
        # # try:
        # #     import docx2pdf
        # # except Exception as e:
        # #     printf(f"Ошибка импорта модуля! Подробнее:\n{e}"); ok = False
        # # if ok:
        # input_file = f"./{folder}/{output_file}.docx"
        # output_file1 = f"./{folder}/{output_file}.pdf"
        # self.file_open.write('hi4')
        # # input_file = 'test.docx'
        # # output_file = 'test.pdf'
        # # if not os.path.exists(input_file):
        #     #     printf(f"Файл {input_file} не найден! Выполнение конвертации невозможно!")
        #     # else:
        #     #     docx2pdf.convert(input_file, output_file)
        # self.file_open.write('hi5')
        # try:
        #     docx2pdf.convert(input_file, output_file1)
        # except Exception as e:
        #     import traceback
        #     a = str(traceback.print_exc())
        #     self.file_open.write('hi6')
        #     self.file_open.write(str(e))
        # step = 100
        # self.cal_signal.emit(step)

        #Для LibreOffice на Windows
        # import subprocess
        # docx_path= f"./{folder}/{output_file}.docx"
        # output_dir= f"./{folder}/{output_file}.pdf"
        # if not os.path.exists(libreoffice_path):
        #     libreoffice_path = r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        #     if not os.path.exists(libreoffice_path):
        #         # Конвертация в pdf 2-й способ нужен установленный Word
        #         import sys
        #         import comtypes.client
        #         dirs = sys.executable
        #         wdFormatPDF = 17
        #         # out_file = self.trans_path(dirs, output_file, folder)
        #         out_file = 'D:\\repo\\calibrator\\prj2\csv,docx,pdf\\' + output_file
        #         # for subdir, dirs, files in os.walk(input_dir):
        #         #     printf(subdir,dirs,files)
        #         #     for file in files:
        #         #         in_file = os.path.join(subdir, file)
        #         # output_file = file.split('.')[0]
        #         # out_file = output_dir + output_file +'.pdf'
        #         word = comtypes.client.CreateObject('Word.Application')
        #         doc = word.Documents.Open(out_file + '.docx')
        #         doc.SaveAs(out_file + '.pdf', FileFormat=wdFormatPDF)
        #         doc.Close()
        #         word.Quit()
        #         # raise FileNotFoundError(f"LibreOffice executable not found at: {libreoffice_path}")
        #
        # # Создает директорию
        # # if not os.path.exists(output_dir):
        # #     os.makedirs(output_dir)
        # command = [
        #     libreoffice_path,
        #     "--headless",  # Run LibreOffice without a graphical interface
        #     "--convert-to", "pdf",
        #     "--outdir", folder,
        #     docx_path
        # ]
        #
        # try:
        #     subprocess.run(command, check=True, capture_output=True, text=True)
        #     print(f"Successfully converted '{docx_path}' to PDF in '{output_dir}'.")
        # except subprocess.CalledProcessError as e:
        #     print(f"Error during conversion: {e}")
        #     print(f"Stdout: {e.stdout}")
        #     print(f"Stderr: {e.stderr}")
        # except FileNotFoundError:
        #     print(f"Error: LibreOffice executable not found at {libreoffice_path}.")


        # Для LibrOffice где установлен Linux
        # import subprocess
        #
        # input_docx= f"./{folder}/{output_file}.odt"
        # output_pdf= f"./{folder}/{output_file}.pdf"
        #
        # # Команда для конвертации с помощью LibreOffice
        # command = [
        #     "soffice",
        #     "--headless",  # Работа в режиме "без головы" (без графического интерфейса)
        #     "--convert-to",
        #     "pdf",
        #     "--outdir",
        #     ".",  # Каталог, куда будет сохранен PDF
        #     input_docx
        # ]
        #
        # # try:
        # subprocess.run(command, check=True, capture_output=True)
        # print(f"Файл '{input_docx}' успешно конвертирован в '{output_pdf}'")
        # # except FileNotFoundError:
        # #     print("Ошибка: LibreOffice (soffice) не найден. Убедитесь, что он установлен.")
        # # except subprocess.CalledProcessError as e:
        # #     print(f"Ошибка при конвертации: {e}")
        # #     print(f"Stderr: {e.stderr.decode()}")
        # step = 100
        # self.cal_signal.emit(step)


    # Из пути делает абсолютный путь, т.е. добавляет еще один '\'
    def trans_path(self,dir,out_file,folder):
        inp = ''
        cnt =0
        printf(dir.count('\\'))
        for i in dir:
            # print(i)
            if cnt==dir.count('\\'):break
            if i =='\r':
                i ='\/\\r'
            inp +=i
            if i =='\\':
                inp +='\\'
                cnt+=1
        printf(inp)
        # inp += f'\/\\{out_file}'
        # inp = inp.replace('/','')
        inp +=f'{folder}\\\{out_file}'
        return inp


class Param(QWidget):

    def __init__(self,param_dict,unit,size_stacked):
        super().__init__()

        self.initUI(param_dict,unit,size_stacked)

    def initUI(self,param_dict,unit,size_stacked):
        self.cnt_elem = 0
        self.size_stacked = size_stacked
        # Шрифт
        self.font = QtGui.QFont()
        self.font.setFamily("Times New Roman")
        # font.setBold(True)
        # font.setWeight(75)
        # self.centralwidget = centr
        # self.centralwidget.setObjectName("centralWidget")

        # Порт
        # self.page = QtWidgets.QWidget()
        # self.page.setObjectName("page")
        # self.page.setGeometry(QtCore.QRect(300,300,300,300))

        # self.horizontWidget = QtWidgets.QWidget(self.page)
        # self.horizontWidget.setGeometry(QtCore.QRect(20, 20, 210, 40))
        # self.horizontWidget.setObjectName("horizontWidget")
        self.horizontLayout = QtWidgets.QHBoxLayout()
        self.horizontLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontLayout.setObjectName("horizontLayout")
        # self.horizontLayout.addStretch(1)
        # self.horizontLayout.setContentsMargins(0, 0, 0, 0)
        # self.horizontLayout.setObjectName("horizontLayout")

        self.centr_widget = QtWidgets.QWidget()
        self.centr_widget.setGeometry(QtCore.QRect(600,600,600,600))

        self.data_tab =QtWidgets.QTabWidget()
        # model = QtGui.QStandardItemModel()
        # table = QtWidgets.QTableView()
        # item1 = QtGui.QStandardItem('EA_F_U_A')
        # item2 = QtGui.QStandardItem('Частота')
        # item3 = QtGui.QStandardItem(str(0))
        # item1.setTextAlignment(QtCore.Qt.AlignCenter)
        # item3.setTextAlignment(QtCore.Qt.AlignCenter)
        # model.appendRow([item1, item2, item3])
        # # model.setHorizontalHeaderLabels(['Обозначение', 'Наименование', 'Значение'])
        # table.setModel(model)
        # table.setRowHeight(0,10)
        # table.setColumnWidth(0, 80)
        # table.setColumnWidth(1, 100)
        # table.setColumnWidth(2, 74)
        # table.setFont(font)
        # table.horizontalHeader().hide()
        # table.verticalHeader().hide()
        # table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # data_tab.setStyleSheet('background-color:rgb(220,254,225);')
        # table.setStyleSheet('background-color:rgb(220,254,225);')
        # self.widget = QtWidgets.QWidget(self.centr_widget)
        # self.widget.setContentsMargins(400,0,0,0)
        # self.widget.setGeometry(0,0,750,330)
        # self.widget.setGeometry(QtCore.QRect(0,500,0,0))
        # self.vbox = QtWidgets.QVBoxLayout(self.widget)
        # self.vbox.addWidget(QtWidgets.QLabel('Таблица 1'))
        # self.vbox.addWidget(table)

        # model1 = QtGui.QStandardItemModel()
        # table1 = QtWidgets.QTableView()
        # self.item =[]
        # for i in range (1,4):
        #     item1 = QtGui.QStandardItem(f'N_I_B{i}')
        #     item2 = QtGui.QStandardItem(f'Ток{i}')
        #     self.item3 = QtGui.QStandardItem(str(i))
        #     item1.setTextAlignment(QtCore.Qt.AlignCenter)
        #     self.item3.setTextAlignment(QtCore.Qt.AlignCenter)
        #     self.item3.setBackground(QtGui.QBrush(QtGui.QColor(255,255,9)))
        #     self.item.append(item1)
        #     self.item.append(item2)
        #     self.item.append(self.item3)
        #     # model1.appendRow([item1, item2, self.item3])
        #     model1.appendRow([item1,item2,self.item3])
        # # model.setHorizontalHeaderLabels(['Обозначение', 'Наименование', 'Значение'])
        # table1.setModel(model1)
        # table1.setColumnWidth(0, 80)
        # table1.setColumnWidth(1, 100)
        # table1.setColumnWidth(2, 74)
        # table1.setRowHeight(0,10)
        # table1.setFont(font)
        # table1.horizontalHeader().hide()
        # table1.verticalHeader().hide()
        # printff(model1.item(1,0).text())
        # table1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # table1.setGridStyle(0)

        # self.widget1 = QtWidgets.QWidget(self.centr_widget)
        # self.vbox1 = QtWidgets.QVBoxLayout(self.widget1)
        # self.vbox1.addWidget(QtWidgets.QLabel('Таблица 2'))
        # self.vbox1.addWidget(table1)

        # data_tab.addTab(self.centr_widget, "Вкладка 1")
        # data_tab.setCurrentIndex(0)
        # data_tab.setStyleSheet('background-color:rgb(220,254,225);')\
                               #gridline-color:black;')
        # table1.setStyleSheet('background-color:rgb(220,254,225);')

        # self.widget2 = QtWidgets.QWidget(self.centr_widget)
        # self.widget2.setContentsMargins(400,400,0,0)
        # self.widget.setGeometry(0,0,750,330)
        # self.vbox2 = QtWidgets.QVBoxLayout(self.centr_widget)
        # self.vbox2.setGeometry(QtCore.QRect(100,100,200,300))


        # for i in range(0,3):
        #     fon_metric = self.lst_widget[i].fontMetrics().width(text)
        #     printff(fon_metric)
        #     if fon_metric > 268:
        #         printff('fon_m')
        #         # self.list_widget.resize(290,35)
        #         self.lst_widget[i].setGeometry(10, 10 + i, 290, 40)
        #         self.lst_widget1[i].setGeometry(300, 10 + i, 100, 40)
        #         self.lst_widget_item1[i].setSizeHint(QtCore.QSize(10, 40))
        #     else:
        #         self.lst_widget[i].setGeometry(10, 10 + i, 290, 20)
        #         self.lst_widget1[i].setGeometry(300, 10 + i, 100, 20)

        # params = [1, 2, 3,4,5,6]
        # text = ['Параметры уставки калибровки классы %']
        # text1 = 'Параметры уставки калибровки классы аt'
        # text1 = list(text1)
        # if text1[35] == ' ':
        #     text1[35] = '\n'
        # text1 = ''.join(text1)
        # printff(text1)
        # param_dicts = self.count_keys(param_dict[unit])
        # printff(param_dicts,len(param_dict[unit]))
        # printff(len(param_dict[unit].items()),param_dict[unit])

        param_obj = []

        for elem in param_dict[unit].items():
            j = [j for j in elem[1].values()]
            param_obj.append(('head',elem[0]))
            for i in j:
                param_obj.append(('name',i[0]))
        printf(param_dict[unit])
        printf(param_obj)

        len_for = round(((len(param_obj)*20/self.size_stacked)/2)+0.5)
        # printff(len_for,len(param_obj),self.size_stacked)
        arg =(0,0)
        self.lst_widget = []
        self.lst_widget1 = []
        self.lst_widget_item1 = []
        for i in range(0,len_for):
            i+=1
            self.widget = QtWidgets.QWidget(self.centr_widget)
            self.data_tab.addTab(self.widget, f"Вкладка {i}")
            # printff(self.size_stacked)
            self.widget.setGeometry(
            QtCore.QRect(self.size_stacked, self.size_stacked, self.size_stacked, self.size_stacked))

            self.data_tab.setCurrentIndex(0)
            self.data_tab.setStyleSheet('background-color:rgb(220,254,225);')
            if arg!=None:
                arg = self.add_List_half(10, 10, 300, 10, param_obj, arg[0],arg[1])
                # printff(arg)
            if arg!=None:
                arg = self.add_List_half(450, 10, 740, 10, param_obj, arg[0], arg[1])
        # if arg !=None:
        #     arg = self.add_List_half(450, 10, 740, 10, param_obj, arg[0],arg[1])
        #     if unit == 'BU_50':
        #         self.add_List(10, 10, 300, 10, param_obj, arg[0], arg[1])

        # arg = self.add_List(10, 10, 300, 10, param_obj, 0,0)
        # printff(arg)
        # if arg !=None:
        #     arg = self.add_List(10, 10, 300, 10, param_obj, arg[0],arg[1])
        #     if unit == 'BU_50':
        #         self.add_List(10, 10, 300, 10, param_obj, arg[0], arg[1])


        # self.add_List_View(10, 10, 300, 10, params, text)
        # self.add_List_View(450, 10, 740, 10, params, text)

        #QListView
        # self.listView = QtWidgets.QListView(self.centr_widget)
        # self.model  = QtCore.QStringListModel()
        # self.model.setStringList(text)
        # self.listView.setModel(self.model)
        # self.listView.setGeometry(10,10,290,40)
        # self.listView.setFont(self.font)
        # self.listView.setStyleSheet('background-color:rgb(255,255,255);')
        # self.listView.setWordWrap(True)
        # # self.listView.setWrapping(True)
        # self.listView.setResizeMode(self.listView.Adjust)
        # self.listView.setItemAlignment(QtCore.Qt.AlignBottom)
        # self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # index = self.listView.currentIndex()
        # self.listView.scrollTo(index ,hint=QtWidgets.QAbstractItemView.PositionAtTop)
        # # self.listView.scroll()
        # fon_metric = self.listView.fontMetrics().width(text[0])
        # printff(fon_metric)
        # printff(len(text[0]))

        self.horizontLayout.addWidget(self.data_tab)
        # table1.clicked.connect(self.selectRow)
        # model1.itemChanged.connect(self.on1_click)
        self.setLayout(self.horizontLayout)
        # printf('Unit2')

    def add_List_half(self,x1,y1,x2,y2,param_obj,start_while,text_label):
        # printff('func add_list_half')

        k = 0
        z = 0
        fon_metric = 0
        flag = 0
        size_all_widget = 0

        for i in range(start_while,len(param_obj)):
            self.cnt_elem+=1
            j = i*20
            if start_while!=0:
                j-=start_while*20

            if size_all_widget+20 > self.widget.size().height() and param_obj[i][0] == 'head':
                size_all_widget += self.label.size().height()

            if size_all_widget > self.widget.size().height():
                # printff(i,text_label)
                return i, text_label

            if param_obj[i][0] == 'head':
                # printff(param_obj[i][1], param_obj[i][0])
                self.label = QtWidgets.QLabel(self.widget)
                if fon_metric <= 269:
                    if j == 0:
                        self.label.setGeometry(x1 + 3, y1 + j + k, 390, 20)
                    else:
                        # printff(j, z, k)
                        z += 5
                        self.label.setGeometry(x1 + 3, y1 + j + z + k, 390, 20)
                else:
                    self.label.setGeometry(x1 + 3, y1 + j + j + k, 390, 20)
                size_all_widget += self.label.size().height()
                text_label = param_obj[i][1]
                self.label.setText(text_label)
                self.font.setPointSize(14)
                self.label.setFont(self.font)
                self.font.setPointSize(11)
            elif param_obj[i][0] == 'name':
                # if flag == 1 and flag2 == 0:
                #     self.label = QtWidgets.QLabel(self.widget)
                #     printff()
                #     self.label.setGeometry(x1 + 3, y1 + j + k, 390, 20)
                #     self.label.setText(text_label)
                #     self.font.setPointSize(14)
                #     self.label.setFont(self.font)
                #     self.font.setPointSize(11)
                #     flag2 = 1
                #     size_all_widget += self.label.size().height()
                if start_while == i and start_while != 0:
                    self.label = QtWidgets.QLabel(self.widget)
                    self.label.setGeometry(x1 + 3, y1 + j + k, 390, 20)
                    self.label.setText(text_label)
                    self.font.setPointSize(14)
                    self.label.setFont(self.font)
                    self.font.setPointSize(11)
                    size_all_widget += self.label.size().height()
                    k+=20
                self.list_widget = QtWidgets.QListWidget(self.widget)
                self.list_widget.setFont(self.font)
                fon_metric = self.list_widget.fontMetrics().width(param_obj[i][1])
                self.list_widget.setStyleSheet('background-color:rgb(255,255,255);')
                text1 = self.trans_str(fon_metric, param_obj[i][1])
                self.listWidgetItem = QtWidgets.QListWidgetItem(text1[0])
                self.list_widget.addItem(self.listWidgetItem)
                # printff(fon_metric,text1[0],i)
                # self.list_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
                # self.list_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                # self.list_widget.itemChanged.connect(self.text_changed)
                # self.list_widget.setWordWrap(True)
                # self.listWidgetItem.setTextAlignment(QtCore.Qt.AlignCenter)

                self.list_widget1 = QtWidgets.QListWidget(self.widget)
                # self.listWidgetItem1 = QtWidgets.QListWidgetItem("0")
                self.listWidgetItem1 = QtWidgets.QListWidgetItem(str(self.cnt_elem))
                self.list_widget1.addItem(self.listWidgetItem1)
                # self.list_widget1.setFrameShape(QtWidgets.QFrame.NoFrame)
                # self.list_widget1.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.list_widget1.setStyleSheet('background-color:rgb(255,255,255);')
                self.list_widget1.setFont(self.font)
                # printff(self.list_widget1.width())
                self.listWidgetItem1.setTextAlignment(QtCore.Qt.AlignCenter)
                self.lst_widget.append(self.list_widget)
                self.lst_widget1.append(self.list_widget1)
                self.lst_widget_item1.append(self.listWidgetItem1)
                # printff(fon_metric)
                # printf(self.list_widget.item(0).text(),fon_metric)
                if fon_metric <= 279:
                    # printff(j, z, k, text1[0])
                    if flag == 0:
                        self.list_widget.setGeometry(x1, y1 + j + z + k, 290, 20)
                        self.list_widget1.setGeometry(x2, y2 + j + z + k, 100, 20)
                    else:
                        self.list_widget.setGeometry(x1, y1 + j + z + k, 290, 20)
                        self.list_widget1.setGeometry(x2, y2 + j + z + k, 100, 20)

                else:
                    # printff(j, z, k, text1[0])
                    if k == 0:
                        # # if j == 0 and flag == 1:
                        # #     printff()
                        # #     self.list_widget.setGeometry(x1, y1 + j + z + 20, 290, 35)
                        # #     self.list_widget1.setGeometry(x2, y2 + j + z + 20, 100, 35)
                        # #     self.listWidgetItem1.setSizeHint(QtCore.QSize(10, 35))
                        # #     k += 15
                        # else:
                        self.list_widget.setGeometry(x1, y1 + j + z, 290, 35)
                        self.list_widget1.setGeometry(x2, y2 + j + z, 100, 35)
                        self.listWidgetItem1.setSizeHint(QtCore.QSize(10, 35))
                        k = +15
                    else:
                        self.list_widget.setGeometry(x1, y1 + j + z + k, 290, 35)
                        self.list_widget1.setGeometry(x2, y2 + j + z + k, 100, 35)
                        self.listWidgetItem1.setSizeHint(QtCore.QSize(10, 35))
                        k += 15
                    # self.list_widget.setGeometry(x1, y1 + j + z , 290, 35)
                    # self.list_widget1.setGeometry(x2, y2 + j + z, 100, 35)
                    # self.listWidgetItem1.setSizeHint(QtCore.QSize(10, 35))

                size_all_widget += self.list_widget.size().height()

        lst_temp = []
        for i in self.lst_widget_item1:
            lst_temp.append(i.text())

        # self.lst_widget_item1[0].setText('5')
        printf(lst_temp)

    def add_List(self,x1,y1,x2,y2,param_obj,start_while,text_label):
        printf('func add_list')

        self.widget= QtWidgets.QWidget(self.centr_widget)
        printf(self.size_stacked)
        self.widget.setGeometry(QtCore.QRect(self.size_stacked,self.size_stacked,self.size_stacked,self.size_stacked))

        self.data_tab.addTab(self.widget, "Вкладка 1")
        self.data_tab.setCurrentIndex(0)
        self.data_tab.setStyleSheet('background-color:rgb(220,254,225);')

        k=0
        z =0
        fon_metric =0
        flag=0
        flag2=0
        size_all_widget = 0



        # for i in range(0,self.count_keys(param_dict)+len(param_dict)):
        printf(len(param_obj))
        for i in range(start_while,len(param_obj)):
            j = i*20
            if start_while!=0:
                j-=start_while*20

            if size_all_widget+20 > self.widget.size().height() and param_obj[i][0] == 'head':
                size_all_widget += self.label.size().height()
                flag2=1
                # j-=20
                printf(j)
                printf(size_all_widget+20,self.label.size().height(),self.widget.size().height())

            if size_all_widget >self.widget.size().height() and flag ==0:
                printf(size_all_widget,self.label.size().height(),self.widget.size().height())
                tmp = j
                x1 = 450
                x2 = 740
                j =0
                k =0
                z =0
                flag =1
                size_all_widget =0
            elif flag == 1:
                j-=tmp
                if size_all_widget >self.widget.size().height():
                    printf(i)
                    return i,text_label
            elif start_while!=0:
                j+=20
            if param_obj[i][0] == 'head':
                printf(param_obj[i][1],param_obj[i][0])
                self.label = QtWidgets.QLabel(self.widget)
                if fon_metric<=269:
                    if j ==0:
                        self.label.setGeometry(x1 + 3, y1 + j+k, 390, 20)
                    else:
                        printf(j,z,k)
                        z+=5
                        self.label.setGeometry(x1 + 3, y1 + j+z+k, 390, 20)
                else:
                    self.label.setGeometry(x1 + 3, y1 + j+j+k, 390, 20)
                size_all_widget+=self.label.size().height()
                text_label = param_obj[i][1]
                self.label.setText(text_label)
                self.font.setPointSize(14)
                self.label.setFont(self.font)
                self.font.setPointSize(11)
            elif param_obj[i][0] =='name':
                if flag ==1 and flag2 ==0:
                    self.label = QtWidgets.QLabel(self.widget)
                    printf()
                    self.label.setGeometry(x1 + 3, y1 + j + k, 390, 20)
                    self.label.setText(text_label)
                    self.font.setPointSize(14)
                    self.label.setFont(self.font)
                    self.font.setPointSize(11)
                    flag2 =1
                    size_all_widget+=self.label.size().height()
                elif start_while ==i and start_while !=0:
                    self.label = QtWidgets.QLabel(self.widget)
                    printf()
                    self.label.setGeometry(x1 + 3, y1 + j + k-20, 390, 20)
                    self.label.setText(text_label)
                    self.font.setPointSize(14)
                    self.label.setFont(self.font)
                    self.font.setPointSize(11)
                    size_all_widget+=self.label.size().height()
                self.list_widget = QtWidgets.QListWidget(self.widget)
                self.list_widget.setFont(self.font)
                fon_metric = self.list_widget.fontMetrics().width(param_obj[i][1])
                self.list_widget.setStyleSheet('background-color:rgb(255,255,255);')
                text1 = self.trans_str(fon_metric,param_obj[i][1])
                self.listWidgetItem = QtWidgets.QListWidgetItem(text1[0])
                self.list_widget.addItem(self.listWidgetItem)
                # printff(fon_metric,text1[0],i)
                # self.list_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
                # self.list_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                # self.list_widget.itemChanged.connect(self.text_changed)
                # self.list_widget.setWordWrap(True)
                # self.listWidgetItem.setTextAlignment(QtCore.Qt.AlignCenter)

                self.list_widget1 = QtWidgets.QListWidget(self.widget)
                self.listWidgetItem1 = QtWidgets.QListWidgetItem("0")
                self.list_widget1.addItem(self.listWidgetItem1)
                # self.list_widget1.setFrameShape(QtWidgets.QFrame.NoFrame)
                # self.list_widget1.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.list_widget1.setStyleSheet('background-color:rgb(255,255,255);')
                self.list_widget1.setFont(self.font)
                # printff(self.list_widget1.width())
                self.listWidgetItem1.setTextAlignment(QtCore.Qt.AlignCenter)
                self.lst_widget.append(self.list_widget)
                self.lst_widget1.append(self.list_widget1)
                self.lst_widget_item1.append(self.listWidgetItem1)
                if fon_metric<=299:
                    printf(j,z,k,text1[0])
                    if flag==0:
                        self.list_widget.setGeometry(x1, y1 + j+z+k, 290, 20)
                        self.list_widget1.setGeometry(x2, y2 + j+z+k, 100, 20)
                    else:
                        self.list_widget.setGeometry(x1, y1 + j+z+k+20, 290, 20)
                        self.list_widget1.setGeometry(x2, y2 + j+z+k+20, 100, 20)

                else:
                    printf(j,z,k,text1[0])
                    if k==0:
                        if j ==0 and flag ==1:
                            self.list_widget.setGeometry(x1, y1 + j + z+20, 290, 35)
                            self.list_widget1.setGeometry(x2, y2 + j + z+20, 100, 35)
                            self.listWidgetItem1.setSizeHint(QtCore.QSize(10, 35))
                            k+=15
                        else:
                            self.list_widget.setGeometry(x1, y1 + j+z, 290, 35)
                            self.list_widget1.setGeometry(x2, y2 + j+z, 100, 35)
                            self.listWidgetItem1.setSizeHint(QtCore.QSize(10, 35))
                            k=+15
                    else:
                        self.list_widget.setGeometry(x1, y1 + j+z+k, 290, 35)
                        self.list_widget1.setGeometry(x2, y2 + j+z+k, 100, 35)
                        self.listWidgetItem1.setSizeHint(QtCore.QSize(10, 35))
                        k+=15

                size_all_widget+=self.list_widget.size().height()

    def count_keys(self,d):
        total = 0
        for key, value in d.items():
            if isinstance(value, dict):
                total += self.count_keys(value)
            else:
                total += 1
        return total
    def on1_click(self,value):
        if value.text().isdigit():
            printf('Data',value.text(),value.row())
        else:
            # self.item3.setChild(value.row(),value.column(),self.item3.setText(self.checkValue))
            self.item[2].setChild(value.row(),value.column(),self.item[2].setText(self.checkValue))

    def selectRow(self,data):
        self.checkValue = data.data()
        printf('SELECT',data.row(),data.column(),data.data())

    def text_changed(self):

        printf('text_changed')
        # QTextEdit
        # text = self.list_widget.toPlainText()
        # printff('text',text)
        # metric = QtGui.QFontMetrics(self.list_widget.font())
        # printff('metric',metric)
        # size_font = self.list_widget.rect()
        # printff('size_font',size_font)
        # geom_font = metric.boundingRect(QtCore.QRect(0,0,0,0), QtCore.Qt.TextWordWrap,text)
        # # geom_font = metric.boundingRect(QtCore.QRect(0,0,0,0), QtCore.Qt.WrapAnywhere,text)
        # # geom_font = metric.boundingRect(QtCore.QRect(0,0,0,0), QtGui.QTextOption.WordWrap,text)
        # printff('geom_font',geom_font)
        # x = 10
        # if self.list_widget.fontMetrics().width(text) > size_font.width()-40:
        # # self.list_widget.resize(size_font.width(),geom_font.height()+x)
        #     self.list_widget.resize(size_font.width(),size_font.height()*2)
        # # self.list_widget.resize(size_font.width(), size_font.height())
        # printff(geom_font.width(),geom_font.height())
        # printff(self.list_widget.fontMetrics().width(text))

        # font = self.list_widget.document().defaultFont()
        # fontMetrics = QtGui.QFontMetrics(font)
        # textSize = fontMetrics.size(0, self.list_widget.toPlainText())
        # textHeight = textSize.height() + 30  # Need to tweak
        # self.list_widget.setMaximumHeight(textHeight)

    def trans_str(self,metric,text):
        flag = 0
        # printf(text,metric)
        if metric >279:
            text = list(text)
            for i in range(0,len(text)):
                if i*7>279:
                    if text[i] != ' ':
                        if flag==0:
                            j = i
                            flag=1
                        if flag==1:
                            while(True):
                                j-=1
                                if text[j]==' ':
                                    text[j] = '\n'
                                    break
                            break
                    elif text[i] == ' ':
                        text[i] = '\n'
                        break
            text = ''.join(text)
            # printf(text)
            return [text]
        else: return [text]

    def add_List_View(self,x1,y1,x2,y2,param_dict,text):
        self.lst_widget = []
        self.lst_widget1 = []
        self.lst_widget_item1 = []
        j =0
        for i in range(0,len(param_dict)):
            i*=20
            self.listView = QtWidgets.QListView(self.centr_widget)
            self.listView.setFont(self.font)
            fon_metric = self.listView.fontMetrics().width(text[0])
            printf(fon_metric,text)
            text1 = self.trans_str(fon_metric,text[0])
            self.model  = QtCore.QStringListModel()
            self.model.setStringList(text1)
            self.listView.setModel(self.model)
            self.listView.setStyleSheet('background-color:rgb(255,255,255);')
            self.listView.setResizeMode(self.listView.Adjust)
            self.listView.setItemAlignment(QtCore.Qt.AlignBottom)
            self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

            self.listView1 = QtWidgets.QListView(self.centr_widget)
            self.model  = QtCore.QStringListModel()
            self.model.setStringList(['0'])
            self.listView1.setModel(self.model)
            # self.listView.setGeometry(10,10,290,40)
            self.listView1.setFont(self.font)
            self.listView1.setStyleSheet('background-color:rgb(255,255,255);')
            self.listView1.setResizeMode(self.listView.Adjust)
            # self.listView1.setItemAlignment(QtCore.Qt.AlignBottom)
            self.listView1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            # self.listWidgetItem1.setTextAlignment(QtCore.Qt.AlignCenter)
            self.listView1.setItemAlignment(QtCore.Qt.AlignCenter)

            if fon_metric > 268:
                printf('fon_m',i)
                # self.list_widget.resize(290,35)
                if i ==0:
                    self.listView.setGeometry(x1, y1 + i+i, 290, 35)
                    self.listView1.setGeometry(x2, y2 + i+i, 100, 35)
                else:
                    j+=5
                    self.listView.setGeometry(x1, y1 + i + i-j, 290, 35)
                    self.listView1.setGeometry(x2, y2 + i + i-j, 100, 35)
                # self.listWidgetItem1.setSizeHint(QtCore.QSize(10, 40))
            else:
                self.listView.setGeometry(x1, y1 + i, 290, 20)
                self.listView1.setGeometry(x2, y2 + i, 100, 20)

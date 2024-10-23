__version__='1.0.3' 
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from decimal import *


class MainApp(App):


   # def __init__(self):
   #     self.FONT_SIZE_LABEL =30
   #     self.FONT_SIZE_TEXT =30
   #     #self.FONT_SIZE_LABEL =45
   #     #self.FONT_SIZE_TEXT =90

    def build(self):
       # FONT_SIZE_LABEL =30
       # FONT_SIZE_TEXT =30
        FONT_SIZE_LABEL =45
        FONT_SIZE_TEXT =90
        box_layout = BoxLayout(orientation='vertical')

        box_layout_1 = BoxLayout(orientation='vertical')
        box_layout_2 = BoxLayout(orientation='vertical')
        box_layout_3 = BoxLayout(orientation='horizontal')
        box_layout_4 = BoxLayout(orientation='horizontal')
        box_layout_5 = BoxLayout(orientation='horizontal')
        box_layout_6 = BoxLayout(orientation='horizontal')

        label1 = Label(text='y1, значение', size_hint=(1, 1), font_size=FONT_SIZE_LABEL)
        label2 = Label(text='x1, сырое значение', font_size=FONT_SIZE_LABEL)
        label3 = Label(text='y2, значение', font_size=FONT_SIZE_LABEL)
        label4 = Label(text='x2, сырое значение', font_size=FONT_SIZE_LABEL)
        self.text_input1 = TextInput(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5},
                                     font_size=FONT_SIZE_TEXT, input_filter='float', multiline=False)
        self.text_input2 = TextInput(size_hint=(1, 1), font_size=FONT_SIZE_TEXT,
                                     input_filter='float', multiline=False)
        self.text_input3 = TextInput(size_hint=(1, 1), font_size=FONT_SIZE_TEXT,
                                     input_filter='float', multiline=False)
        self.text_input4 = TextInput(size_hint=(1, 1), font_size=FONT_SIZE_TEXT,
                                     input_filter='float', multiline=False)
        self.btn = Button(text='Расчет', size_hint=(1, 0.7), pos_hint={"center_x": 0.5, "center_y": 0.64},background_color = [1,2,1,1], border = (1,1,1,1),font_size=FONT_SIZE_LABEL)
        self.btn1 = Button(text='Стереть', size_hint=(1, 0.7), pos_hint={"center_x": 0.5, "center_y": 0.64},background_color = [1,2,8,1], border = (1,1,1,1),font_size=FONT_SIZE_LABEL)
        self.text_input5 = TextInput(size_hint=(1, 1.3), font_size=FONT_SIZE_TEXT)

        grid_layout = GridLayout(cols=2)

        box_layout_1.add_widget(label1)
        box_layout_2.add_widget(self.text_input1)
        box_layout_1.add_widget(label2)
        box_layout_2.add_widget(self.text_input2)
        box_layout_1.add_widget(label3)
        box_layout_2.add_widget(self.text_input3)
        box_layout_1.add_widget(label4)
        box_layout_2.add_widget(self.text_input4)
        box_layout_5.add_widget(self.btn1)
        box_layout_5.add_widget(self.btn)
        box_layout_6.add_widget(self.text_input5)

        grid_layout.add_widget(box_layout_1)
        grid_layout.add_widget(box_layout_2)

        box_layout.add_widget(grid_layout)
        box_layout.add_widget(box_layout_5)
        box_layout.add_widget(box_layout_6)

        self.text_input1.bind(text=self.on_text_1)
        self.text_input2.bind(text=self.on_text_2)
        self.text_input3.bind(text=self.on_text_3)
        self.text_input4.bind(text=self.on_text_4)
        self.btn.bind(on_press=self.on_button_press)
        self.btn1.bind(on_press=self.on_button_press1)
        return box_layout

    def on_text_1(self, instance, value):
        self.on_text_1_text = value

    def on_text_2(self, instance, value):
        self.on_text_2_text = value

    def on_text_3(self, instance, value):
        self.on_text_3_text = value

    def on_text_4(self, instance, value):
        self.on_text_4_text = value

    def on_button_press(self, instance):

        try:
            if "." in self.on_text_1_text: 
                y1 = float(self.on_text_1_text)
            else:
                y1 = int(self.on_text_1_text)
            if "." in self.on_text_2_text: 
                x1 = float(self.on_text_2_text)
            else:
                x1 = int(self.on_text_2_text)
            if "." in self.on_text_3_text: 
                y2 = float(self.on_text_3_text)
            else:
                y2 = int(self.on_text_3_text)
            if "." in self.on_text_4_text: 
                x2 = float(self.on_text_4_text)
            else:
                x2 = int(self.on_text_4_text)
            # print('btn:', y1, x1, y2, x2)
            k, b = self.calc_koef(y1, x1, y2, x2)
            # print('k', k, 'b', b)
          #  k = Decimal(str(k))
          #  k = k.quantize(Decimal("1.000000"))
          #  b = Decimal(str(b))
          #  b = b.quantize(Decimal("1.000000"))

            self.text_input5.text =f"{y1} = k * {x1} + b"+ "\n" +f"{y2} = k * {x2} + b"+"\n"\
                    "\nk = " + str(k) + "\n" + "b = " + str(b)
            return 0
        except AttributeError:
            self.text_input5.text = "Ошибка! Заполните все поля"
        except ValueError:
            self.text_input5.text = "Ошибка! Заполните все поля"
        except TypeError:
            self.text_input5.text = "Ошибка! Деление на ноль нельзя"

    def on_button_press1(self, instance):

        self.text_input1.text = ""
        self.text_input2.text = ""
        self.text_input3.text = ""
        self.text_input4.text = ""

        self.text_input5.text =""
        return 0


    def calc_koef(self, y1, x1, y2, x2):
        try:
            k = (y2 - y1) / (x2 - x1)
            if isinstance(y2, float) or isinstance(y1, float) or \
               isinstance(y2, float) or isinstance(y1, float):
                flag =1
                k = Decimal(str(k))
                k = k.quantize(Decimal("1.000000"))
            else:
                flag =2
                k = Decimal(str(k))
                k = k.quantize(Decimal("1.0000"))

            k = float(k)
            b = y2 - k * x2
            if flag ==1:
                b = Decimal(str(b))
                b = b.quantize(Decimal("1.000000"))
            else:
                b = Decimal(str(b))
                b = b.quantize(Decimal("1.0000"))
            b = float(b)
            return k, b
        except ZeroDivisionError:
            self.text_input5.text = "Ошибка! Деление на ноль нельзя"
            return 0


if __name__ == '__main__':
    MainApp().run()

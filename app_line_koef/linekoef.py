# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class MainApp(App):

    def build(self):
        box_layout = BoxLayout(orientation='vertical')

        box_layout_1 = BoxLayout(orientation='vertical')
        box_layout_2 = BoxLayout(orientation='vertical')
        box_layout_3 = BoxLayout(orientation='horizontal')
        box_layout_4 = BoxLayout(orientation='horizontal')
        box_layout_5 = BoxLayout(orientation='horizontal')
        box_layout_6 = BoxLayout(orientation='horizontal')

        label1 = Label(text='y1, значение', size_hint=(1, 1), font_size=25)
        label2 = Label(text='x1, сырое значение', font_size=25)
        label3 = Label(text='y2, значение', font_size=25)
        label4 = Label(text='x2, сырое значение', font_size=25)
        self.text_input1 = TextInput(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5},
                                     font_size=25, input_filter='float', multiline=False)
        self.text_input2 = TextInput(size_hint=(1, 1), font_size=25,
                                     input_filter='float', multiline=False)
        self.text_input3 = TextInput(size_hint=(1, 1), font_size=25,
                                     input_filter='float', multiline=False)
        self.text_input4 = TextInput(size_hint=(1, 1), font_size=25,
                                     input_filter='float', multiline=False)
        self.btn = Button(text='GO!', size_hint=(1, 0.7), pos_hint={"center_x": 0.5, "center_y": 0.64})
        self.text_input5 = TextInput(size_hint=(1, 1.3), font_size=30)

        grid_layout = GridLayout(cols=2)

        box_layout_1.add_widget(label1)
        box_layout_2.add_widget(self.text_input1)
        box_layout_1.add_widget(label2)
        box_layout_2.add_widget(self.text_input2)
        box_layout_1.add_widget(label3)
        box_layout_2.add_widget(self.text_input3)
        box_layout_1.add_widget(label4)
        box_layout_2.add_widget(self.text_input4)
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
            y1 = int(self.on_text_1_text)
            x1 = int(self.on_text_2_text)
            y2 = int(self.on_text_3_text)
            x2 = int(self.on_text_4_text)
            # print('btn:', y1, x1, y2, x2)
            k, b = self.calc_koef(y1, x1, y2, x2)
            # print('k', k, 'b', b)

            self.text_input5.text = "k = " + str(k) + "\n\n" + "b = " + str(b)
            return 0
        except AttributeError:
            self.text_input5.text = "error!"

    def calc_koef(self, y1, x1, y2, x2):
        k = (y2 - y1) / (x2 - x1)
        b = y2 - (x2 * (y2 - y1) / (x2 - x1))
        return k, b


if __name__ == '__main__':
    MainApp().run()

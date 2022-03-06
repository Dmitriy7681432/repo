import random
class Durak:
    def __init__(self):
        #Список карт от 6 до 10
        cards_6_10 = [x for x in range(6, 11)]
        #Список старших карт
        cards_set_1_suit = list(map(str, cards_6_10)) + 'Валет Дама Король Туз'.split()
        #Список мастей
        self.suit = u'\u2660,\u2665,\u2663,\u2666'.split(',')


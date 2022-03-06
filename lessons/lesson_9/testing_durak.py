import random
cards_list =[]
cards_6_10 = [x for x in range(6,11)]
print(cards_6_10)
cards_set_1_suit = list(map(str, cards_6_10)) + 'Валет Дама Король Туз'.split()
print(cards_set_1_suit)
suit = u'\u2660,\u2665,\u2663,\u2666'.split(',')
print(suit)
for i in suit:
    cards_all = [x+suit[suit.index(i)] for x in cards_set_1_suit]
    cards_list =cards_list+cards_all
print(cards_list)
random.shuffle(cards_list)
print(cards_list)

print('-'*30)

#
# cards_set = []
# cards_set_6_10 = [x for x in range(6, 11)] # генерируем список карт от 6 до 10
# # создаем список cards_set_1_suit - карты одной масти
# cards_set_1_suit = list(map(str, cards_set_6_10)) + 'Валет Дама Король Туз'.split()
# # self.suit - 4 масти из Unicode
# suit = u'\u2660,\u2665,\u2663,\u2666'.split(',')
#
# # Делаем словарь cards_dict
# # присваиваем значения ключам - картам одной масти ('6':0, '7':1 и т.д.)
#
# #self._card_deck - словарь полной колоды карт
# _card_deck_dict = {}
# # создаем словарь со значениями для одной масти
# _cards_dict = {cards_set_1_suit[i]: i for i in range(len(cards_set_1_suit))}
# # создаем словарь со значениями для 4 мастей
# for i in range(len(suit)):  # в каждой из 4 мастей
#     for keys, values in _cards_dict.items():  # для каждого ключа словаря
#         keys = suit[i] + keys # ключ - это масть (значок Unicode) и первоначальный ключ('6','7','Валет' и т.д.)
#         print(keys, values)
#         _card_deck_dict[keys] = values #словарь полной колоды карт со значениями
# print('Словарь без козырей:', _card_deck_dict)

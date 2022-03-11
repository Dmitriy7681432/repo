import random
class Durak:
    def __init__(self,nubmer_player=2):
        self.nubmer_pralyer = nubmer_player
        #Список карт от 6 до 10
        cards_6_10 = [x for x in range(6, 11)]
        #Список старших карт
        cards_set_1_suit = list(map(str, cards_6_10)) + 'Валет Дама Король Туз'.split()
        #Список мастей
        self.suit = u'\u2660,\u2665,\u2663,\u2666'.split(',')
        self._cards_list = []
        for i in self.suit:
            cards_all = [x + self.suit[self.suit.index(i)] for x in cards_set_1_suit]
            self._cards_list = self._cards_list + cards_all
        # random.shuffle(self.cards_list)
    #Перемешивание карт
    def shhuffle(self):
        random.shuffle(self._cards_list)
        print('Карты перемешены')
    #Раздача карт
    def distribution_of_cards(self):
        self.card_player_1 = self._cards_list[-6:]
        self.card_player_2 = self._cards_list[-12:-6]
        del self._cards_list[-12:]
    #Определение козыря
    def trump_card(self):
        self.trump = self._cards_list.pop()
        self._cards_list.insert(-1,self.trump)
        print('Козырь:',self.trump)

    #Количество карт в колоде
    def count_cards(self):
        print(f'Количество карт в колоде: {len(self._cards_list)}')

    def players_move(self):
        if random.randint(1,2) ==1:
            print('Ходит Игрок 1')
            return 'Ходит Игрок 1'
        else:
            print('Ходит Игрок 2')
            return 'Ходит Игрок 2'

    def player_move(self):



    def __str__(self):
        return self.cards_list

#Начало игры
game = Durak()
#Перемешивание карт
game.shhuffle()
print(game._cards_list)
#Раздача карт
game.distribution_of_cards()
print(game.card_player_1)
print(game.card_player_2)
print(game._cards_list)
#Определение козыря
game.trump_card()
#Количество карт в колоде
game.count_cards()
#Кто ходит первым
turn_start = game.players_move()






# class Card:
#     def __init__(self):
#         self.ip = '1,2,3,4'
#     def __str__(self):
#         return self.ip
# card = Card()
# print(card)
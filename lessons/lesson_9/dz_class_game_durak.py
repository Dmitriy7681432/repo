import random,traceback,sys
def func():
    stack = traceback.extract_stack()
    print('Print from {}'.format(stack[-2][2]))

class Durak:
    def __init__(self,nubmer_player=2):
        self.nubmer_player = nubmer_player
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
        self.flag =0
        #Карты участвующие в процессе игры Игрока 1
        self.movie_ls = []
        #Карты участвующие в процессе игры Игрока 2
        self.answer2_ls = []
    #Перемешивание карт
    def shhuffle(self):
        random.shuffle(self._cards_list)
        # print('Карты перемешены')

    #Раздача карт
    def distribution_of_cards(self):
        self.card_player_1 = self._cards_list[-6:]
        self.sorted_cards(self.card_player_1)
        self.card_player_2 = self._cards_list[-12:-6]
        self.sorted_cards(self.card_player_2)
        del self._cards_list[-12:]

    # Сортировка карт
    def sorted_cards(self,a):
        for i in range(len(a)):
            if a[i] == '10'+u'\u2660':
                a[i] = 'A'+ u'\u2660'
            if a[i] == '10'+u'\u2665':
                a[i] = 'A'+ u'\u2665'
            if a[i] == '10'+u'\u2663':
                a[i] = 'A'+ u'\u2663'
            if a[i] == '10'+u'\u2666':
                a[i] = 'A'+ u'\u2666'
        a.sort()
        for i in range(len(a)):
            if a[i] == 'A' + u'\u2660':
                a[i] = '10' + u'\u2660'
            if a[i] == 'A' + u'\u2665':
                a[i] = '10' + u'\u2665'
            if a[i] == 'A' + u'\u2663':
                a[i] = '10' + u'\u2663'
            if a[i] == 'A' + u'\u2666':
                a[i] = '10' + u'\u2666'
        # print('Отсортировано',a)

    #Определение козыря
    def trump_card(self):
        self.trump = self._cards_list.pop()
        self._cards_list.insert(-1,self.trump)
        print('Козырь:',self.trump)

    #Количество карт в колоде
    def count_cards(self):
        print(f'Количество карт в колоде: {len(self._cards_list)}')
        if len(self._cards_list):
            return 'Карты закончались'
    #Кто ходит первым
    def players_move(self):
        if random.randint(1,2) ==1:
            self.player=1
            print('Ходит Игрок 1')
            return 'Ходит Игрок 1'
        else:
            self.player=2
            print('Ходит Игрок 2')
            return 'Ходит Игрок 2'

    #Ход игрока 1
    def player_move(self):
        if self.flag==1:
            if not self.answer2[:-1] in ''.join(self.card_player_1):
                self.flag=0
                self.movie_ls.clear()
                self.answer2_ls.clear()
                print('Бита',sys._getframe().f_lineno)
                return "Бита"
        print('Карты игрока 1', self.card_player_1,sys._getframe().f_lineno)
        print('Ход игрока 1')
        a = int(input())
        if a >=0 and self.flag ==0:
            self.movie = self.card_player_1.pop(a)
            self.movie_ls.append(self.movie)
            print(self.movie,sys._getframe().f_lineno)
            print('Карты игрока 1',self.card_player_1,sys._getframe().f_lineno)
            self.flag=1
        elif a>=0 and self.flag==1: #and self.card_player_1[0][:-1]==self.answer2[:-1]:
            self.movie = self.card_player_1.pop(a)
            self.movie_ls.append(self.movie)
            print(self.movie,sys._getframe().f_lineno)
            print('Карты игрока 1', self.card_player_1,sys._getframe().f_lineno)
        else:
            print('Не одно условие не верно')
            self.flag =0

    #Ответ игрока 2
    def answer_player2(self):
        print('Карты игрока 2',self.card_player_2,sys._getframe().f_lineno)
        print('Ответ игрока 2',sys._getframe().f_lineno)
        a = int(input())
        if a >=0:
            if (self.card_player_2[a]>self.movie or self.card_player_2[a][:2]=="10")\
                    and self.card_player_2[a][-1:]==self.movie[-1:]:
                print(self.movie,self.card_player_2[a])
                self.answer2 = self.card_player_2.pop(a)
                self.answer2_ls.append(self.answer2)
                print('Карты игрока 2', self.card_player_2,sys._getframe().f_lineno)
            else:
                print(False, 'Бита')
                return 'Бита'
        elif a < 0:
            self.flag=0
            print('Беру')
            print(self.movie_ls)
            for i in self.movie_ls:self.card_player_2.append(i)
            for i in self.answer2_ls:self.card_player_2.append(i)
            self.movie_ls.clear()
            self.answer2_ls.clear()
            self.sorted_cards(self.card_player_2)
            print('Карты Игрока 2',self.card_player_2,sys._getframe().f_lineno)
            return 'Беру'

    # Ход игрока 2
    def player_move2(self):
        if self.flag == 1:
            if not self.answer2[:-1] in ''.join(self.card_player_2):
                self.flag = 0
                self.movie_ls.clear()
                self.answer2_ls.clear()
                print('Бита', sys._getframe().f_lineno)
                return 'Бита'
        print('Карты игрока 2', self.card_player_2, sys._getframe().f_lineno)
        print('Ход игрока 2')
        a = int(input())
        if a >=0 and self.flag == 0:
            self.movie = self.card_player_2.pop(a)
            self.movie_ls.append(self.movie)
            print(self.movie, sys._getframe().f_lineno)
            print('Карты игрока 2', self.card_player_2, sys._getframe().f_lineno)
            self.flag = 1
        elif a >= 0 and self.flag == 1:
            self.movie = self.card_player_2.pop(a)
            self.movie_ls.append(self.movie)
            print(self.movie, sys._getframe().f_lineno)
            print('Карты игрока 2', self.card_player_2, sys._getframe().f_lineno)
        else:
            print('Не одно условие не верно')
            self.flag = 0

    # Ответ игрока 1
    def answer_player(self):
        print('Карты игрока 1', self.card_player_1, sys._getframe().f_lineno)
        print('Ответ игрока 1', sys._getframe().f_lineno)
        a = int(input())
        if a >= 0:
            if (self.card_player_1[a] > self.movie or self.card_player_1[a][:2] == "10") \
                    and self.card_player_1[a][-1:] == self.movie[-1:]:
                print(self.movie, self.card_player_1[a])
                self.answer2 = self.card_player_1.pop(a)
                self.answer2_ls.append(self.answer2)
                print('Карты игрока 1', self.card_player_1, sys._getframe().f_lineno)
            else:
                print(False, 'Бита')
                return 'Бита'
        elif a <0:
            self.flag = 0
            print('Беру')
            print(self.movie_ls)
            for i in self.movie_ls: self.card_player_1.append(i)
            for i in self.answer2_ls: self.card_player_1.append(i)
            self.movie_ls.clear()
            self.answer2_ls.clear()
            self.sorted_cards(self.card_player_1)
            print('Карты Игрока 1', self.card_player_1, sys._getframe().f_lineno)
            return 'Беру'

    def getting_cards(self):
        count_pl1 = 6 - len(self.card_player_1)
        count_pl2 = 6 - len(self.card_player_2)
        if count_pl1>0 and len(self._cards_list)!=0:
            print('Добор карт для игрока 1')
            for i in range(count_pl1):
                if len(game._cards_list)>0:
                    self.card_player_1.append(self._cards_list.pop(0))
        if count_pl2>0 and len(self._cards_list)!=0:
            print('Добор карт для игрока 2')
            for i in range(count_pl2):
                if len(game._cards_list)>0:
                    self.card_player_2.append(self._cards_list.pop(0))
        self.sorted_cards(self.card_player_1)
        self.sorted_cards(self.card_player_2)
        print('Колода карт',self._cards_list,sys._getframe().f_lineno)
        self.count_cards()
        print('Карты Игрока 1',self.card_player_1,sys._getframe().f_lineno)
        print('Карты Игрока 2',self.card_player_2,sys._getframe().f_lineno)
        return 'Карты получены'
# #Начало игры
# game = Durak()
# # #Перемешивание карт
# game.shhuffle()
# #Раздача карт
# game.distribution_of_cards()
# turn_start = game.players_move()
# if turn_start == 'Ходит Игрок 1':
#     turn_movie2 = 0
#     turn_answer = 0
#     while(1):
#         turn_movie = game.player_move()
#         if turn_movie == 'Бита':
#             turn_getting = game.getting_cards()
#             while(1):
#                 if (len(game.card_player_1) == 0 or len(game.card_player_2) == 0) and \
#                         len(game._cards_list) == 0:
#                     print('Переход к концу игры', sys._getframe().f_lineno)
#                     break
#                 turn_movie2 = game.player_move2()
#                 if turn_movie2 == 'Бита':
#                     turn_getting = game.getting_cards()
#                     break
#                 turn_answer = game.answer_player()
#                 if turn_answer == 'Беру':
#                     turn_getting = game.getting_cards()
#                     continue
#         if turn_movie2 == 'Бита' or turn_answer == 'Бита':
#             turn_movie2 = 0
#             turn_answer = 0
#             continue
#         if (len(game.card_player_1) == 0 or len(game.card_player_2)==0) and\
#             len(game._cards_list)==0:
#             print('Конец игры',sys._getframe().f_lineno)
#             if len(game.card_player_1)==0: print("Выиграл Игрок 1")
#             elif len(game.card_player_2)==0: print("Выиграл Игрок 2")
#             break
#         turn_answer2 = game.answer_player2()
#         if turn_answer2 == 'Беру':
#             turn_getting = game.getting_cards()
#
# if turn_start == 'Ходит Игрок 2':
#     turn_movie = 0
#     turn_answer2 = 0
#     while(1):
#         turn_movie2 = game.player_move2()
#         if turn_movie2 == 'Бита':
#             turn_getting = game.getting_cards()
#             while(1):
#                 if (len(game.card_player_1) == 0 or len(game.card_player_2) == 0) and \
#                         len(game._cards_list) == 0:
#                     print('Переход к концу игры', sys._getframe().f_lineno)
#                     break
#                 turn_movie = game.player_move()
#                 if turn_movie == 'Бита':
#                     turn_getting = game.getting_cards()
#                     break
#                 turn_answer2 = game.answer_player2()
#                 if turn_answer2 == 'Беру':
#                     turn_getting = game.getting_cards()
#                     continue
#         if turn_movie == 'Бита' or turn_answer2 == 'Бита':
#             turn_movie = 0
#             turn_answer2 = 0
#             continue
#         if (len(game.card_player_1) == 0 or len(game.card_player_2)==0) and\
#             len(game._cards_list)==0:
#             print('Конец игры',sys._getframe().f_lineno)
#             if len(game.card_player_1)==0: print("Выиграл Игрок 1")
#             elif len(game.card_player_2)==0: print("Выиграл Игрок 2")
#             break
#         turn_answer = game.answer_player()
#         if turn_answer == 'Беру':
#             turn_getting = game.getting_cards()

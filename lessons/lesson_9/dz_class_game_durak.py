import random,traceback
def func():
    stack = traceback.extract_stack()
    print('Print from {}'.format(stack[-2][2]))

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
        self.flag =0
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
        self.movie = []
        if self.flag==1:
            if not self.answer2[:-1] in ''.join(self.card_player_1):
                self.flag=0
                self.movie.clear()
                print('Бита',func())
                return "Ходит Игрок 2"
        print('Карты игрока 1', self.card_player_1,func())
        print('Ход игрока 1')
        a = int(input())
        if a ==0 and self.flag ==0:
            self.movie = self.movie.append(self.card_player_1.pop(0))
            print(self.movie,func())
            print('Карты игрока 1',self.card_player_1,func())
            self.flag=1
        elif a==0 and self.flag==1 and self.card_player_1[0][:-1]==self.answer2[:-1]:
            self.movie.append(self.card_player_1.pop(0))
            print(self.movie,func())
            print('Карты игрока 1', self.card_player_1,func())
        elif a ==1 and self.flag==1 and self.card_player_1[1][:-1]==self.answer2[:-1]:
            self.movie.append(self.card_player_1.pop(1))
            print(self.movie)
            print('Карты игрока 1',self.card_player_1,func())
        elif a ==2 and self.flag==1 and self.card_player_1[2][:-1]==self.answer2[:-1]:
            self.movie.append(self.card_player_1.pop(2))
            print(self.movie,func())
            print('Карты игрока 1',self.card_player_1,func())
        elif a ==3 and self.flag==1 and self.card_player_1[3][:-1]==self.answer2[:-1]:
            self.movie.append(self.card_player_1.pop(3))
            print(self.movie)
            print('Карты игрока 1',self.card_player_1)
        elif a ==4 and self.flag==1 and self.card_player_1[4][:-1]==self.answer2[:-1]:
            self.movie.append(self.card_player_1.pop(4))
            print(self.movie)
            print('Карты игрока 1',self.card_player_1)
        else:
            print('Не одно условие не верно')
            self.flag =0

    #Ответ игрока 2
    def answer_player2(self):
        if self.player_move() == 'Ходит Игрок 2':
            return 'Ходит Игрок 2'
        print('Карты игрока 2',self.card_player_2)
        print('Ответ игрока 2')
        a = int(input())
        if a ==0:
            if (self.card_player_2[0]>self.movie or self.card_player_2[0][:2]=="10")\
                    and self.card_player_2[0][-1:]==self.movie[-1:]:
                print(self.movie,self.card_player_2[0])
                self.answer2 = self.card_player_2.pop(0)
                print('Карты игрока 2', self.card_player_2)
            else:
                print(False)
        elif a ==1:
            if (self.card_player_2[1]>self.movie or self.card_player_2[1][:2]=="10")\
                    and self.card_player_2[1][-1:]==self.movie[-1:]:
                print(self.movie,self.card_player_2[1])
                self.answer2 = self.card_player_2.pop(1)
                print('Карты игрока 2', self.card_player_2)
            else:
                print(False)
        elif a ==2:
            if (self.card_player_2[2]>self.movie or self.card_player_2[2][:2]=="10")\
                    and self.card_player_2[2][-1:]==self.movie[-1:]:
                print(self.movie,self.card_player_2[2])
                self.answer2 = self.card_player_2.pop(2)
                print('Карты игрока 2', self.card_player_2)
            else:
                print(False)
        elif a ==3:
            if (self.card_player_2[3]>self.movie or self.card_player_2[3][:2]=="10")\
                    and self.card_player_2[3][-1:]==self.movie[-1:]:
                print(self.movie,self.card_player_2[3])
                self.answer2 = self.card_player_2.pop(3)
                print('Карты игрока 2', self.card_player_2)
            else:
                print(False)
        elif a ==4:
            if (self.card_player_2[4]>self.movie or self.card_player_2[4][:2]=="10")\
                    and self.card_player_2[4][-1:]==self.movie[-1:]:
                print(self.movie,self.card_player_2[4])
                self.answer2 = self.card_player_2.pop(4)
                print('Карты игрока 2', self.card_player_2)
            else:
                print(False)
        elif a ==5:
            if (self.card_player_2[5]>self.movie or self.card_player_2[5][:2]=="10")\
                    and self.card_player_2[5][-1:]==self.movie[-1:]:
                print(self.movie,self.card_player_2[5])
                self.answer2 = self.card_player_2.pop(5)
                print('Карты игрока 2', self.card_player_2)
            else:
                print(False)
        elif a ==6:
            if (self.card_player_2[6]>self.movie or self.card_player_2[6][:2]=="10")\
                    and self.card_player_2[6][-1:]==self.movie[-1:]:
                print(self.movie,self.card_player_2[6])
                self.answer2 = self.card_player_2.pop(6)
                print('Карты игрока 2', self.card_player_2)
            else:
                print(False)
        elif a ==7:
            if (self.card_player_2[7]>self.movie or self.card_player_2[7][:2]=="10")\
                    and self.card_player_2[7][-1:]==self.movie[-1:]:
                print(self.movie,self.card_player_2[7])
                self.answer2 = self.card_player_2.pop(7)
                print('Карты игрока 2', self.card_player_2)
            else:
                print(False)
        elif a ==-1:
            self.flag=0
            print('Беру')
            self.card_player_2.append(self.movie)
            self.sorted_cards(self.card_player_2)
            print('Карты Игрока 2',self.card_player_2)
            return 'Бита'

    def getting_cards(self):
        count_pl1 = 6 - len(self.card_player_1)
        count_pl2 = 6 - len(self.card_player_2)
        if count_pl1>0:
            for i in range(count_pl1):
                self.card_player_1.append(self._cards_list.pop(0))
        elif count_pl2>0:
            for i in range(count_pl2):
                self.card_player_2.append(self._cards_list.pop(0))
        self.sorted_cards(self.card_player_1)
        self.sorted_cards(self.card_player_2)
        print('Колода карт',self._cards_list)
        print('Карты Игрока 1',self.card_player_1)
        print('Карты Игрока 2',self.card_player_2)
        return 'Карты получены'
#Начало игры
game = Durak()
#Перемешивание карт
game.shhuffle()
#Раздача карт
game.distribution_of_cards()
# print('Игрок 1',game.card_player_1)
# print('Игрок 2',game.card_player_2)
# print('Общая колода',game._cards_list)
#Сортировка карт
# game.sorted_cards(game.card_player_1)
# print('Игрок 1 отсортирован',game.card_player_1)
#Определение козыря
# game.trump_card()
#Количество карт в колоде
# game.count_cards()
#Кто ходит первым
turn_start = game.players_move()
# movie_pl1 = game.player_move()
if turn_start == 'Ходит Игрок 1':
    while(1):
        turn_movie = game.player_move()
        if turn_movie =='Ходит Игрок 2':
            print('Выход из цикла')
            break
        if turn_movie == 'Бита':
            turn_getting = game.getting_cards()
        turn_answer2 = game.answer_player2()
        if turn_answer2 == 'Бита':
            turn_getting = game.getting_cards()

# if turn_start == 'Ходит Игрок 2':



# class Card:
#     def __init__(self):
#         self.ip = '1,2,3,4'
#     def __str__(self):
#         return self.ip
# card = Card()
# print(card)
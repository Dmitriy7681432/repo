import pytest
from lessons.lesson_9.dz_class_game_durak import Durak


class TestDurak:

    def setup(self):
        self.game = Durak()
        print("Start Test")

    def teartdown(self):
        print("The end Test")

    def test_init(self):
        print('Сборка')
        assert self.game.nubmer_player==2

    def test_counts_cards(self):
        assert len(self.game._cards_list) == 36

# def func1():
#     a = 3
#     b = 4
#     c = a+b
#     print('AA')
#     assert c ==7
#     return c
# func1()
# assert func1()==7
# test_d = TestDurak()
# test_d.test_init()

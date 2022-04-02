import pytest
from lessons.lesson_9.dz_class_game_durak import Durak


class TestDurak:

    def setup(self):
        pass

    def teartdown(self):
        pass

    def test_init(self):
        game = Durak()
        assert game.nubmer_player==2


def func1():
    a = 3
    b = 4
    c = a+b
    assert c ==7
    return c
func1()
# assert func1()==7
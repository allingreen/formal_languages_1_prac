import pytest

from main import Parser, ParserException


class Tests:

    def test_irregular(self):
        regular = 'a*.'
        k = 4
        x = Parser(regular, k)
        with pytest.raises(ParserException):
            x.get_answer(3)

    def test_1(self):
        regular = 'ab+c.aba.*.bac.+.+*'
        k = 3
        x = Parser(regular, k)
        assert x.get_answer(0) == 0
        assert x.get_answer(1) == 4
        assert x.get_answer(2) == 2

    def test_2(self):
        regular = 'acb..bab.c.*.ab.ba.+.+*a.'
        k = 3
        x = Parser(regular, k)
        assert x.get_answer(0) == 'INF'
        assert x.get_answer(1) == 1
        assert x.get_answer(2) == 'INF'

    def test_3(self):
        regular = 'aa.aaa..+*'
        k = 10
        x = Parser(regular, k)
        assert x.get_answer(0) == 0
        assert x.get_answer(1) == 11
        assert x.get_answer(2) == 2
        assert x.get_answer(3) == 3
        assert x.get_answer(4) == 4
        assert x.get_answer(5) == 5
        assert x.get_answer(6) == 6
        assert x.get_answer(7) == 7
        assert x.get_answer(8) == 8
        assert x.get_answer(9) == 9

    def test_4(self):
        regular = 'ab.*'
        k = 4
        x = Parser(regular, k)
        assert x.get_answer(0) == 0
        assert x.get_answer(1) == 'INF'
        assert x.get_answer(2) == 2
        assert x.get_answer(3) == 'INF'

    def test_5(self):
        regular = 'ba.'
        k = 4
        x = Parser(regular, k)
        assert x.get_answer(0) == 'INF'
        assert x.get_answer(1) == 'INF'
        assert x.get_answer(2) == 2
        assert x.get_answer(3) == 'INF'

    def test_6(self):
        regular = 'aa.b*.'
        k = 5
        x = Parser(regular, k)
        assert x.get_answer(0) == 5
        assert x.get_answer(1) == 6
        assert x.get_answer(2) == 2
        assert x.get_answer(3) == 3
        assert x.get_answer(4) == 4

    def test_7(self):
        regular = 'ab+'
        k = 4
        x = Parser(regular, k)
        assert x.get_answer(0) == 'INF'
        assert x.get_answer(1) == 1
        assert x.get_answer(2) == 'INF'
        assert x.get_answer(3) == 'INF'


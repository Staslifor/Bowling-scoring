import unittest

from bowling.bowling import game_score, International, Native, score_for_test

_test_data = """1/6/1/--327-18812382
X53232/3/62--62Х
725518Х--8/--543152
8/--35-47/371/518-4/
4-3/7/3/8/Х711627-5"""


class GameTest(unittest.TestCase):

    def test_bowling(self):
        for_test_native = []
        for_test_international = []
        for _ in _test_data.split('\n'):
            result_native = game_score(Native, _)
            result_international = game_score(International, _)
            for_test_native.append(result_native)
            for_test_international.append(result_international)
        self.assertEqual(for_test_native, [90, 99, 83, 96, 113])
        self.assertEqual(for_test_international, [82, 86, 68, 84, 111])

    def test_exc(self):
        self.assertRaises(Exception, score_for_test(Native, 'Ш532X332/3/62--62X'))
        self.assertRaises(Exception, score_for_test(International, 'Ш532X332/3/62--62X'))

    def test_exc_BL(self):
        self.assertRaises(Exception, score_for_test(Native, '99X332/3/62--62X'))
        self.assertRaises(Exception, score_for_test(International, '99X332/3/62--62X'))

    def test_exc_ME(self):
        self.assertRaises(Exception, score_for_test(Native, '3X32X332/3/62--62X'))
        self.assertRaises(Exception, score_for_test(International, '3X32X332/3/62--62X'))


if __name__ == '__main__':
    unittest.main()

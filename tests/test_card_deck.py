from unittest import TestCase
from src.card_deck import *


class TestCard(TestCase):
    def test_card_creation(self):
        self.assertEqual(Card('4h').card, '4❤')
        self.assertEqual(Card('4H').card, '4❤')
        self.assertEqual(Card('4❤').card, '4❤')
        self.assertEqual(Card('10D').card, '10♦')

    def test_suit_attr(self):
        self.assertEqual(Card('10D').suit, '♦')
        self.assertEqual(Card('A♦').suit, '♦')
        self.assertEqual(Card('JH').suit, '❤')

    def test_value_attr(self):
        self.assertEqual(Card('10D').value, '10')
        self.assertEqual(Card('QC').value, 'Q')
        self.assertEqual(Card('AS').value, 'A')

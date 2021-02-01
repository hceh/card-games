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


class TestCardDeck(TestCase):

    def test_n_cards(self):
        # todo:
        #  basic deck = 52
        #  other examples tested
        self.fail()

    def test_creation(self):
        # todo:
        #  standard pack
        #  jokers
        #  >1 decks
        #  mix
        self.fail()

    def test_shuffle(self):
        # todo:
        #  compare slices of shuffled deck to initial deck, check diff
        #  check set of before and after same
        #  check n_cards same between two
        self.fail()

    def test_draw_card(self):
        # todo: check that what is drawn is a card
        #  card was in the deck
        #  card is no longer in deck
        self.fail()

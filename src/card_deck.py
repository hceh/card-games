import random
from datetime import datetime

from numpy import arange
from time import sleep


class Card:
    """
    generic card class, with suit and value attributes
    """

    def __init__(self, card: str):
        """
        takes string input for card in form 4H or 4h, converts suit to symbol
        """
        self.value = card[:-1]
        self.suit = self.__convert_suit(card[-1])
        self.card = f'{self.value}{self.suit}'

    def __repr__(self):
        return self.card

    def __getitem__(self, item):
        return self.card[item]

    @staticmethod
    def __convert_suit(card: str) -> str:
        """
        converts letter suit (upper/lower) and returns corresponding symbol
        """
        suit = card[-1]
        d_suits = {'H': '❤', 'D': '♦', 'C': '♣', 'S': '♠'}
        return suit if suit in d_suits.values() else d_suits[card[-1].upper()]


class Hand:
    def __init__(self, cards: list):
        """
        takes list of type Card to initiate hand of cards
        """
        self.cards = cards
        self.__value_order = {str(k): v for v, k in enumerate(list(arange(2, 11)) + ['J', 'Q', 'K', 'A'])}

    @property
    def n_cards(self) -> int:
        """
        get number of cards in hand
        """
        return len(self.cards)

    def show(self):
        """
        unhidden method to show cards in hand - use quick show to be able to hide output in console
        """
        return self.cards

    def quick_show(self, secs=2):
        """
        shows hand for :secs: seconds, then clears and replaces with *'s
        """
        print(self.cards, end='\r')
        sleep(secs)  # todo: would rather end by pressing enter but breaks the clearing
        print('********')

    def organise_by_value(self):
        """
        organises cards in hand according to value then suit, aces high
        """
        self.cards = sorted(self.cards, key=lambda x: (self.__value_order[getattr(x, 'value')], getattr(x, 'suit')))

    def organise_by_suit(self):
        """
        organises cards in hand according to suit then value, aces high
        """
        self.cards = sorted(self.cards, key=lambda x: (getattr(x, 'suit'), self.__value_order[getattr(x, 'value')]))

    def add_card(self, card: Card):
        """
        add card of type Card to hand
        """
        self.cards.append(card)

    def play_card(self, card: str):
        """
        remove and return card (str), to be used when putting down single cards to table
        use in conjunction with and method from a CardDeck or Table that receives a single card eg RummyTable.play_card
        """
        if type(card) == str:
            card = Card(card)
        if card not in self.cards:
            raise AttributeError("you don't hold this card!")
        self.cards.remove(card)
        return card


class Player:
    """
    generic player class
    """

    def __init__(self, hand, name: str = None, dealer: bool = False):
        self.hand = hand
        self.name = name
        self.dealer = dealer

    def __repr__(self):
        return self.name


class CardDeck:
    """
    generic card deck
    """

    def __init__(self, hand_type=Hand, jokers: bool = False, n_decks: int = 1):
        """
        initiate deck of :n_decks: to return hands of type :hand_type: (Hand, RummyHand)
        adds 2 jokers per pack according to :jokers:
        """
        self._values = [str(_) for _ in arange(2, 11)] + ['J', 'Q', 'K', 'A']
        self._suits = ['❤', '♦', '♣', '♠']
        self.cards = [Card(f'{val}{suit}') for suit in self._suits for val in self._values]
        if jokers:
            self.cards.extend([Card('J1'), Card('J2')])
        self.cards *= n_decks
        self.hand_type = hand_type
        self.status = f'Deck created at {datetime.now().strftime("%H:%M:%S")}'

    @property
    def n_cards(self):
        """
        return number of cards in deck
        """
        return len(self.cards)

    def shuffle(self):
        """
        shuffle deck and update deck status
        """
        random.shuffle(self.cards)
        print('cards shuffled')
        self.status += f'\nDeck shuffled at {datetime.now().strftime("%H:%M:%S")}'

    def deal(self, n_cards: int, n_hands: int = 2) -> list:
        """
        deal number of cards n_cards to number of hands n_hands of type hand_type specified in deck initialisation

        if you attempt to deal more cards than are in the deck, it will deal as many as possible equally between each
        hand

        returns list of hand_type objects
        """
        if (dealt_cards := n_cards * n_hands) > self.n_cards:
            n_cards = self.n_cards // n_hands
            print(f"you're trying to deal too many cards, have only dealt {n_cards}")
        hand_list = list()
        for h in range(n_hands):
            hand = self.hand_type([self.cards[(_ * n_hands) + h] for _ in range(n_cards)])
            hand_list.append(hand)
        self.cards = self.cards[dealt_cards:]
        print(f'dealt {n_hands} hands of {n_cards} cards')
        return hand_list

    def draw_card(self):
        """
        remove and return top card in pack
        """
        card = self.cards.pop(0)
        print(f'You picked up {card}')
        return card


class Table:
    """
    generic table class
    """

    def __init__(self):
        """
        single attribute card_pile for discarded cards
        """
        self.card_pile = list()

    @property
    def n_cards(self):
        """
        return number of cards in discard pile
        """
        return len(self.card_pile)

    @property
    def top_card(self):
        """
        return top card on discard pile
        """
        if self.n_cards == 0:
            return 'no cards played'
        else:
            return self.card_pile[-1]

    def pick_up_card(self):
        """
        returns top card from discard pile if exists
        """
        if self.n_cards == 0:
            raise AttributeError('no cards left on the pile, please draw from deck')
        else:
            card = self.card_pile.pop(-1)
            return card


if __name__ == '__main__':
    table = Table()
    deck = CardDeck()
    deck.shuffle()
    p1, p2 = deck.deal(10, 2)

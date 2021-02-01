from numpy import arange
from pandas import DataFrame

from card_deck import Card, Hand, CardDeck, Table


def leaderboard(player_list: list):
    d_players = {p.name: [p.hand.points] for p in player_list}
    l = DataFrame.from_dict(d_players, orient='index', columns=['Score'])
    l = l.sort_values('Score')
    print(l)


def valid_run(cards: list) -> bool:
    """
    takes unsorted list of cards or strings, checks whether they are a valid run, ie
        - [5H, 6H, 7H]
        - [9D, 10D, JD, QD]
    """
    cards = [Card(_) if type(_) == str else _ for _ in cards]
    suits = [_.suit for _ in cards]

    set_values = [str(_) for _ in arange(2, 11)] + ['J', 'Q', 'K', 'A']
    value_order = {k: v for v, k in enumerate(set_values)}

    cards = sorted(cards, key=lambda x: (value_order[getattr(x, 'value')], getattr(x, 'suit')))

    def is_sub(sub: list, lst: list) -> bool:
        ln = len(sub)
        for i in range(len(lst) - ln + 1):
            if all(sub[j] == lst[i + j] for j in range(ln)):
                return True
        return False

    suits_same = len(set(suits)) == len(suits)

    values_in_order = is_sub([c.value for c in cards], set_values)

    enough_cards = len(cards) >= 3

    return all([suits_same, values_in_order, enough_cards])


def valid_set(cards: list) -> bool:
    """
    takes list of cards or strings, checks whether they are a valid set, ie
        - [4H, 4D, 4C]
        - [AH, AC, AS, AD]
    """
    cards = [Card(_) if type(_) == str else _ for _ in cards]
    suits = [_.suit for _ in cards]
    values = [_.value for _ in cards]

    suits_unique = len(set(suits)) == len(suits)
    values_same = len(set(values)) == 1
    enough_cards = len(cards) >= 3

    return all([suits_unique, values_same, enough_cards])


class RummyTable(Table):
    """
    Superclass of Table, with rummy specific attributes and behaviours
    """

    def __init__(self):
        super().__init__()
        self.sets_played = list()  # cards played face up to table

    @property
    def n_cards(self) -> int:
        """
        returns number of cards on table, within discard pile and sets played
        """
        return len(self.card_pile) + sum([len(_) for _ in self.sets_played])

    def show_table(self):
        """
        shows all cards currently on table
        """
        print(f'Top Card: {self.top_card}\n\nSets played:')
        for i, s in enumerate(self.sets_played):
            print(f'{i + 1}: {s}')

    def play_card(self, card: str):
        """
        plays a card to the discard pile, used in conjunction with Hand.play_card
        """
        self.card_pile.append(card)

    def play_set(self, cards: list):
        """
        plays a new set of cards to the table, receiving the set from RummyHand.play_set
        """
        self.sets_played.append(cards)

    def return_discard_pie_to_draw_pile(self):
        """
        for use when all cards in deck have been drawn, and all but the top card are reused, passed to
        RummyDeck.reset_draw_pile
        """
        top_card = self.top_card
        discard_pile = self.card_pile[:-1]
        self.card_pile = list(top_card)
        return discard_pile

    def add_to_set(self, cards: list, set_index: int):
        """
        adds set of cards passed from RummyHand.play_set and adds to set shown by RummyTable.show_table by index,
        validating new output is a valid set or run, printing outcome
        """
        try:
            initial_set = self.sets_played[set_index - 1]  # -1 as sets are numbered 1 up in show_table
        except IndexError:
            raise IndexError('this set number does not exist!')
        cards = [Card(_) if type(_) == str else _ for _ in cards]
        new_set = initial_set + cards
        if not any([valid_set(new_set), valid_run(new_set)]):
            raise AttributeError('new set is not valid set or run!')
        self.sets_played[set_index - 1] = new_set
        print(f'Set updated: {initial_set} > {new_set}')


class RummyHand(Hand):
    """
    Superclass of Hand, with methods specific to Rummy, like playing sets and adding to sets on the table
    """

    def __init__(self, cards):
        super().__init__(cards)

    def play_set(self, *cards):
        """
        plays a valid set of cards or runs, to be used in conjunction with RummyTable.play_set
        """
        to_play = [Card(_) if type(_) == str else _ for _ in cards]
        if not set(to_play).issubset(self.cards):
            raise AttributeError("you don't hold all these cards")
        if not any([valid_run(to_play), valid_set(to_play)]):  # check cards are run or set
            raise AttributeError("this isn't a valid set or run of 3 or more cards")
        for card in to_play:
            self.cards.remove(card)
        return to_play

    def lay_off(self, *cards):
        """
        lay off  cards to be added to a set already on the table, checking cards are held and removing them from hand.
        to be used in conjunction with RummyTable.add_to_set
        """
        to_play = [Card(_) if type(_) == str else _ for _ in cards]
        if not set(to_play).issubset(self.cards):
            raise AttributeError("you don't hold all these cards")
        for card in to_play:
            self.cards.remove(card)
        return to_play

    @property
    def has_won(self):
        """
        test for if hand is complete and player has won
        """
        return self.n_cards == 0

    @property
    def num_points(self):
        """
        returns number of points left in hand
        """
        non_val_points = {'A': '1', 'J': '10', 'Q': '10', 'K': '10'}
        values = [_.value for _ in self.cards]
        values = [non_val_points[_] if _ in non_val_points else _ for _ in values]
        values = [int(_) for _ in values]
        return sum(values)


class RummyDeck(CardDeck):
    """
    Superclass of CardDeck that sets the requirements for dealing, and has rummy specific methods
    """

    def __init__(self):
        super().__init__(RummyHand, jokers=False, n_decks=1)

    def reset_draw_pile(self, discarded_cards, shuffle=True):
        """
        When all cards in draw pile used up, take all but top card from discard pile, shuffle and add to
        deck draw pile.
        Usage:
            deck.reset_draw_pile(table.return_discard_pile_to_draw_pile())
        """
        self.cards = discarded_cards
        if shuffle:
            self.shuffle()


if __name__ == '__main__':
    table = RummyTable()
    deck = RummyDeck()
    deck.shuffle()
    n_players = int(input('How many players?  '))  # add player construct with name, dealer bool etc?
    players = deck.deal(10, n_players)
    while not any([p.has_won for p in players]):
        pass  # play the game
    leaderboard(players)

""" Defines the base classes from which most entities in a game can be derived. """


class Game:
    """ 'God' class which describes the game itself. Often the game itself is the owner of some entities, it usually
    also takes some kind of Actor-role (e.g. when a deck of cards shared between players is reshuffled).
    It also contains the `GameTable` which should comprise all entities which are physically present and shall be
    rendered in any fashion. """
    def __init__(self):
        self.table = None


class GameTable:
    """ Abstract representation of the table the game is played on. It contains all other physical entities visible
    to all players, it is also the 'canvas' on which the visualization is rendered.
    If something shall be drawn in the UI, it must be placed somewhere on the game table. """
    def __init__(self, width, height):
        self._width = width
        self._height = height


class Actor:
    """ Abstract actor in the game, e.g. a player, an automated enemy, etc. """
    pass


class Player(Actor):
    """ One of the game participants in a classical sense, normally controlled by a Human. """
    pass


class PhysicalEntity:
    """ Base class for all entities which physically exist somewhere on the game table. """
    pass


class Card(PhysicalEntity):
    def __init__(self, owner):
        self.owner = owner


class Token(PhysicalEntity):
    """ Physical token which is somehow part of the game. Normally these are small plastic figures, bricks, and similar
    things which mark either a counter or the location of something in the game (e.g. a building on a specific tile).
    The `owner` is usually an `Actor`."""
    def __init__(self, owner):
        self.owner = owner


class Sheet(PhysicalEntity):
    """ Rectangular piece of paper, cardboard, or plastic which is part of the game. Usually has some graphic to be
    drawn and may also contain `Slot`s for other entities such as tokens or cards. """
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self.slots = {}

    def add_slot(self, identifier, rect):
        """ Defines a slot with the given `rect` area (expressed in percentages of the Sheet's own size.
        The slot can be identified via the identifier for easier access. """
        self.slots[identifier] = Slot(self, rect)


class Slot:
    """ Designated rectangular area on a sheet on which tokens, cards, etc. can be placed. """
    def __init__(self, owner, rect):
        self._owner = owner
        self._rect = rect

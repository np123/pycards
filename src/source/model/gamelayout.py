"""This module defines the interface for game classes

    State Variables: none

    Environment Variables: none

    Assumptions: none

"""

from abc import ABCMeta, abstractmethod, abstractproperty


class CardGame():
    """Abstract base class to be used as specification for all games"""
    __metaclass__ =  ABCMeta

    _bindings = None

    @classmethod
    def __subclasshook__(cls, subclass):
        pass

    @abstractmethod
    def create(self):
        """
        Define the initial layout of the game including
        the number and positioning of cards

        Also place restriction on the allowed actions based
        on the rules of the game

        **Must be implemented by subclass**
        """

    @abstractmethod
    def deal(self):
        """
        If in-game dealing is allowed this performs
        a single deal action

        **Must be implemented by subclass**
        """

    @abstractmethod
    @abstractproperty
    def bindings(self):
        """Return the mouse bindings the game needs

        **Must be implemented by subclass**
        """
        global _bindings
        if _bindings is None:
            return NotImplementedError("Must define bindings and accessor in game subclass")


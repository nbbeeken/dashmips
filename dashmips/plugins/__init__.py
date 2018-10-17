"""Plugins for dashmips."""

from abc import ABC, abstractmethod
from threading import Thread


class Plugin(ABC):
    """Abstract Plugin."""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def pull(self, *changes):
        """Call to react to changed variables."""
        raise NotImplementedError('Abstract method.')

    @abstractmethod
    def push(self, changes):
        """Call to change variables."""
        raise NotImplementedError('Abstract method.')

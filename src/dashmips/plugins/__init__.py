"""Plugins for dashmips."""
from abc import ABC, abstractmethod
from typing import Any


class Plugin(ABC):
    """Abstract Plugin."""

    def __init__(self, name: str) -> None:
        """Dashmips Plugin Base Class."""
        self.name = name

    @abstractmethod
    def pull(self, *changes: Any) -> None:
        """Call to react to changed variables."""
        raise NotImplementedError("Abstract method.")

    @abstractmethod
    def push(self, changes: Any) -> None:
        """Call to change variables."""
        raise NotImplementedError("Abstract method.")

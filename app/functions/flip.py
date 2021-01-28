"""Flip module."""

import random


class Base:
    """Defining base class for inheritence."""

    def flip(self):
        """Flip a coin, Heads and Tails."""
        return random.choice(['Heads', 'Tails'])

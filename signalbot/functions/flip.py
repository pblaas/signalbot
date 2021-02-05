"""Flip module."""

import random


class Flip:
    """Defining base class for inheritence."""

    @staticmethod
    def flip():
        """Flip a coin, Heads and Tails."""
        return random.choice(['Heads', 'Tails'])

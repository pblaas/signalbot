"""Haiku module."""

from random import randint


class Haiku:
    """Defining base class for inheritence."""

    @staticmethod
    def haiku():
        """Return a random generator Haiku."""
        wordlist1 = ["Enchanting", "Amazing", "Colourful", "Delightful", "Delicate"]
        wordlist2 = ["visions", "distance", "conscience", "process", "chaos"]
        wordlist3 = ["superstitious", "contrasting", "graceful", "inviting", "contradicting", "overwhelming"]
        wordlist4 = ["true", "dark", "cold", "warm", "great"]
        wordlist5 = ["scenery", "season", "colours", "lights", "Spring", "Winter", "Summer", "Autumn"]
        wordlist6 = ["undeniable", "beautiful", "irreplaceable", "unbelievable", "irrevocable"]
        wordlist7 = ["inspiration", "imagination", "wisdom", "thoughts"]

        wordindex1 = randint(0, len(wordlist1) - 1)
        wordindex2 = randint(0, len(wordlist2) - 1)
        wordindex3 = randint(0, len(wordlist3) - 1)
        wordindex4 = randint(0, len(wordlist4) - 1)
        wordindex5 = randint(0, len(wordlist5) - 1)
        wordindex6 = randint(0, len(wordlist6) - 1)
        wordindex7 = randint(0, len(wordlist7) - 1)

        haiku = wordlist1[wordindex1] + " " + wordlist2[wordindex2] + ",\n"
        haiku = haiku + wordlist3[wordindex3] + " " + wordlist4[wordindex4] + " " + wordlist5[wordindex5] + ",\n"
        haiku = haiku + wordlist6[wordindex6] + " " + wordlist7[wordindex7] + "."

        return haiku

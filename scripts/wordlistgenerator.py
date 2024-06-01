#!/usr/bin/env python
import itertools
import sys
from tkinter import W


def hunter_wordlist_generator():
    """
    Generates a wordlist based on given characters and length constraints.

    Returns:
        None
    """
    characters = input("Characters: ")
    output = open("passwords.txt", W)
    min_length = int(input("Minimum Length: "))
    max_length = int(input("Maximum Length: "))
    for n in range(min_length, max_length + 1):
        for xs in itertools.product(characters, repeat=n):
            chars = "".join(xs)
            output.write("%s\n" % chars)
            sys.stdout.flush()

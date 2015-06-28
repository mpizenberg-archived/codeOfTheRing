#!/usr/bin/env python3

def letterToNumber(letter):
    if(letter==" "):
        return 0
    else:
        return ord(letter)-64

def distance(letter1, letter2):
    l1 = letterToNumber(letter1)
    l2 = letterToNumber(letter2)
    to2 = (l2-l1)%27
    to1 = -((l1-l2)%27)
    if (abs(to2) <= abs(to1)):
        return to2
    else:
        return to1

class Runes:
    
    def __init__(self, letters):
        self.letters = letters

if(__name__ == "__main__"):
    r = Runes([" ", " ", " "])
    print(r.letters)

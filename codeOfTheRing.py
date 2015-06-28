#!/usr/bin/env python3

def letterToNumber(letter):
    if(letter==" "):
        return 0
    else:
        return ord(letter)-64

def ringDistance(pos1, pos2, ringSize):
    to2 = (pos2-pos1)%ringSize
    to1 = -((pos1-pos2)%ringSize)
    if (abs(to2) <= abs(to1)):
        return to2
    else:
        return to1

def letterDistance(letter1, letter2):
    l1 = letterToNumber(letter1)
    l2 = letterToNumber(letter2)
    return ringDistance(l1, l2, 27)

class Runes:
    
    def __init__(self, nb):
        self.letters = [" "]*nb
        self.currentRuneNumber = 0
        self.runeNumber = nb
        self.motionSpell = ""
        self.alreadySpelled = ""
        self.runeState = [" "]

    def reset(self):
        self.__init__(self.runeNumber)

    def changeRuneCost(self, runePos, newLetter):
        oldLetter = self.letters[runePos]
        return abs(ringDistance(self.currentRuneNumber, runePos, self.runeNumber))\
                + abs(letterDistance(oldLetter,newLetter))\
                + 1

    def changeRune(self, runePos, newLetter):
        # rune motion first
        rd = ringDistance(self.currentRuneNumber, runePos, self.runeNumber)
        motionCharacter = ">" if rd>0 else "<"
        runeMotion = motionCharacter * abs(rd)
        # now letter motion
        ld = letterDistance(self.letters[runePos], newLetter)
        letterCharacter = "+" if ld>0 else "-"
        letterMotion = letterCharacter * abs(ld)
        # get full sequence of actions
        motion = runeMotion + letterMotion + "."
        # update current rune
        self.currentRuneNumber = runePos
        # update letters
        self.letters[runePos] = newLetter
        # update motion spell
        self.motionSpell += motion
        # update already spelled
        self.alreadySpelled += newLetter

    # Strategy 1 : stay on first rune and change letter
    def applyStrategy1(self, spell):
        for c in spell:
            self.changeRune(0,c)
            self.runeState[0] = c

    # Strategy 2 : never change letter
    def applyStrategy2(self, spell):
        for c in spell:
            if (c in self.runeState):
                pos = self.runeState.index(c)
            else:
                pos = len(self.runeState)
                self.runeState.append(c)
            self.changeRune(pos, c)

    # Strategy 3 : fastest for next letter
    def applyStrategy3(self, spell):
        # temporary cost table
        costs = [0] * self.runeNumber
        for c in spell:
            for pos,letter in enumerate(self.letters):
                costs[pos] = self.changeRuneCost(pos, c)
            # make the lower cost move
            pos = costs.index(min(costs))
            self.changeRune(pos, c)

if(__name__ == "__main__"):
    r = Runes(30)
    r.changeRune(0,"A")
    r.changeRune(0,"C")
    r.changeRune(0,"F")
    r.changeRune(0,"A")
    r.changeRune(0,"F")
    r.changeRune(0,"A")
    r.changeRune(0,"F")
    print("Strategy 1: " + r.motionSpell)
    r.reset()
    r.applyStrategy1("ACFAFAF")
    print("Strategy 1: " + r.motionSpell)
    r.reset()
    r.changeRune(1,"A")
    r.changeRune(2,"C")
    r.changeRune(3,"F")
    r.changeRune(1,"A")
    r.changeRune(3,"F")
    r.changeRune(1,"A")
    r.changeRune(3,"F")
    print("Strategy 2: " + r.motionSpell)
    r.reset()
    r.applyStrategy2("ACFAFAF")
    print("Strategy 2: " + r.motionSpell)
    r.reset()
    r.changeRune(0,"A")
    r.changeRune(0,"C")
    r.changeRune(0,"F")
    r.changeRune(1,"A")
    r.changeRune(0,"F")
    r.changeRune(1,"A")
    r.changeRune(0,"F")
    print("Strategy 3: " + r.motionSpell)
    r.reset()
    r.applyStrategy3("ACFAFAF")
    print("Strategy 3: " + r.motionSpell)
    r.reset()

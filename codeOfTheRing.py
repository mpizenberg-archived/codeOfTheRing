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
        self.letters = [" "]*nb     # state of all runes
        self.currentRuneNumber = 0  # current rune number
        self.runeNumber = nb        # nb of runes
        self.motionSpell = ""       # motion for the spell
        self.alreadySpelled = ""    # portion of the spell already spelled
        self.runeState = [" "]

    def reset(self):
        self.__init__(self.runeNumber)

    def changeRuneCost(self, runePos, newLetter):
        oldLetter = self.letters[runePos]
        return abs(ringDistance(self.currentRuneNumber, runePos, self.runeNumber))\
                + abs(letterDistance(oldLetter,newLetter))\
                + 1

    def changeRuneSimulate(self, runePos, newLetter):
        """Do not modify motionSpell and alreadySpelled.
        """
        rd = ringDistance(self.currentRuneNumber, runePos, self.runeNumber)
        ld = letterDistance(self.letters[runePos], newLetter)
        self.currentRuneNumber = runePos
        self.letters[runePos] = newLetter
        return abs(rd) + abs(ld) + 1

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
        return abs(rd) + abs(ld) + 1

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

    # Strategy 4 : fastest for 2 next letters
    def applyStrategy4(self, spell):
        # temporary cost table
        costs = [0] * self.runeNumber
        index_l2 = [0] * self.runeNumber
        costs_temp = [0] * self.runeNumber
        # group letters by 2
        spell_2 = [spell[n:n+2] for n in range(0, len(spell), 2)]
        # work on pairs of letters (except maybe last letter)
        for pair in spell_2:
            # if last letter
            if len(pair)==1:
                for pos,letter in enumerate(self.letters):
                    costs_temp[pos] = self.changeRuneCost(pos, pair[0])
                # make the lower cost move
                pos = costs_temp.index(min(costs_temp))
                self.changeRune(pos, pair[0])
            # else if normal pair
            else:
                # save current state of self
                letters = self.letters[:]
                currentRuneNumber = self.currentRuneNumber
                # first simulate changement of first letter then find best change for second letter
                for pos,letter in enumerate(self.letters):
                    # operate computation
                    costs[pos] = self.changeRuneSimulate(pos,pair[0])
                    for pos2,letter2 in enumerate(self.letters):
                        costs_temp[pos2] = self.changeRuneCost(pos2, pair[1])
                    pos2 = costs_temp.index(min(costs_temp))
                    index_l2[pos] = pos2
                    costs[pos] += costs_temp[pos2]
                    # reset as if we did not make any change
                    self.letters = letters[:]
                    self.currentRuneNumber = currentRuneNumber
                # find best pair motion
                pos = costs.index(min(costs))
                self.changeRune(pos, pair[0])
                self.changeRune(index_l2[pos], pair[1])


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
    r.applyStrategy3("UMNE TALMAR RAHTAINE NIXENEN UMIR")
    print("Strategy 3: " + r.motionSpell)
    r.reset()
    r.applyStrategy4("UMNE TALMAR RAHTAINE NIXENEN UMIR")
    print("Strategy 4: " + r.motionSpell)
    r.reset()

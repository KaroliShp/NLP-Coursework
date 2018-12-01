# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
        # Dictionary for storing the lexicon
        # Structure: { category : [word1, word2]}
        self.lexicon_dictionary = {'P':[], 'N':[], 'A':[], 'I':[], 'T':[]}

    def add(self, stem, cat):
        # When category is already a key in the dictionary, add stem to list
        if cat in self.lexicon_dictionary:
            words_list = self.lexicon_dictionary[cat]
            words_list.append(stem)
            self.lexicon_dictionary[cat] = words_list
        else:
            return 'Tag is invalid'

    def getAll(self, cat):
        if not (cat in self.lexicon_dictionary):
            return 'Not a valid tag'
        # This removes duplicates
        return list(set(self.lexicon_dictionary[cat]))

class FactBase:
    """stores unary and binary relational facts"""
    def __init__(self):
        self.unary_facts = []
        self.binary_facts = []

    def addUnary(self, pred, e1):
        self.unary_facts.append((pred, e1))

    def addBinary(self, pred, e1, e2):
        self.binary_facts.append((pred, (e1, e2)))

    def queryUnary(self, pred, e1):
        return (pred, e1) in self.unary_facts

    def queryBinary(self, pred, e1, e2):
        return (pred, (e1, e2)) in self.binary_facts

import re
from nltk.corpus import brown
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # Extract the stem
    # Note - re.match() only matches at the start of the string
    stem = ''
    if s == 'has':
        stem = 'have'
    elif re.match(r'^[a-z]*(?![sxyz(ch)(sh)aeiou])[a-z]s$', s.lower()):
        stem = s[:-1]
    elif re.match(r'^[a-z]*[aeiou]ys$', s.lower()):
        stem = s[:-1]
    elif len(s) > 4 and re.match(r'^[a-z]*(?![aeiou])[a-z]ies$', s.lower()):
        stem = s[:-3] + 'y'
    elif len(s) == 4 and re.match(r'(?![aeiou])[a-z]ies$', s.lower()):
        stem = s[:-1]
    elif re.match(r'^[a-z]*[o|x|(ch)|(sh)|(ss)|(zz)]es$', s.lower()):
        stem = s[:-2]
    elif re.match(r'^[a-z]*(?![s])[a-z]ses$', s.lower()) or re.match(r'^[a-z]*(?![z])[a-z]zes$', s.lower()):
        stem = s[:-1]
    elif re.match(r'^[a-z]*(?![iosxz(ch)(sh)])[a-z]es$', s.lower()):
        stem = s[:-1]
    else:
        return ""

    # Validate that the word is used as a stem
    if (s == 'have' or s == 'are' or s == 'do'):
        return stem;

    for b in brown.tagged_words():
        if (b[1] != 'VBZ' and b[1] != 'VB'):
            continue
        elif (b[0] == stem and b[1] == 'VB'):
            return stem
        elif (b[0] == s and b[1] == 'VBZ'):
            return stem

    return ""

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg

# End of PART A.

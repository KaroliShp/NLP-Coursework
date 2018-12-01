# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    # Does every NN or NNS have corresponding pairs?
    nouns_nn = []
    nouns_nns = []
    unchanging_list = []
    with open("sentences.txt", "r") as f:
        for line in f:
            # Split sentence on space
            for wt in line.split(' '):
                # Split on delimiter on words and tag
                w = wt.split('|')[0]
                t = wt.split('|')[1]
                if w in unchanging_list:
                    continue
                elif (t == 'NN'):
                    if w in nouns_nns:
                        unchanging_list.append(w)
                    else:
                        nouns_nn.append(w)
                elif (t == 'NNS'):
                    if w in nouns_nn:
                        unchanging_list.append(w)
                    else:
                        nouns_nns.append(w)
    return unchanging_list

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""
    stem = ''
    if s in unchanging_plurals_list:
        stem = s
    elif re.match(r'^[a-zA-Z]*men$', s.lower()):
        stem = s[:-2] + 'an'
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
        stem = ""

    return stem

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    common_nouns = lx.getAll("N")
    intransitive_verbs = lx.getAll("I")
    transitive_verbs = lx.getAll("T")
    proper_names = lx.getAll("P")
    adjectives = lx.getAll("A")

    possible_tags = []

    # Check open classes
    if wd in proper_names:
        possible_tags.append('P')
    if wd in adjectives:
        possible_tags.append('A')
    if noun_stem(wd) in common_nouns:
        possible_tags.append('Np')
    if wd in common_nouns:
        possible_tags.append('Ns')
    if verb_stem(wd) in intransitive_verbs:
        possible_tags.append('Is')
    if wd in intransitive_verbs:
        possible_tags.append('Ip')
    if verb_stem(wd) in transitive_verbs:
        possible_tags.append('Ts')
    if wd in transitive_verbs:
        possible_tags.append('Tp')

    # Check function words
    for f in function_words_tags:
        if f[0] == wd:
            possible_tags.append(f[1])

    return possible_tags

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.

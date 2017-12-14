import sys
import string
from MarkovChains import *
from random import randint

#word_count = int(sys.argv[1])
#word_count = randint(10,70)
word_count = 250
sentence_len = 140

def gen(corpus):
    
    #build markov model
    myMC = Markov(corpus)
    words = myMC.file_to_words()
    triplets = myMC.triples()
    db = myMC.database()
    
    #generate, modify, then return text
    genStr = myMC.generate_markov_text(word_count)
    safeTermIndx = 0
    startOffset = 0
    foundStart = False
    foundTerm = False
    
    termList = ".?!"
    for indx in range(len(genStr)):
        if indx >= (startOffset+sentence_len): # stop & check if sentence length is valid
            if not foundTerm: # Go to next start token and try again
                foundStart = False
                foundTerm = False
                indx = startOffset+1
                #print "Term not found, trying again..."
                continue
            else:
                break
        if (not foundStart) and genStr[indx].isupper(): # must start on uppercase
            startOffset = indx
            foundStart = True
            #print "Start token %s found at %s" % (genStr[indx], indx)
        if (genStr[indx] in termList) and genStr[indx+1] in string.whitespace: # must end on conclusion punctuation
            safeTermIndx = indx
            foundTerm = True
            #print "Term token %s found at %s" % (genStr[indx], indx)
    
    if (foundStart and foundTerm):
        genStr = genStr[startOffset:safeTermIndx+1]
    elif foundStart and not foundTerm:
        genStr = genStr[startOffset:startOffset+sentence_len]
    elif not foundStart and foundTerm:
        genStr = genStr[0:startOffset]
    else:
        genStr = genStr[0:sentence_len]
    return genStr

#print "[%s, %s]" % (startOffset, safeTermIndx)


f=open('corpus') #open corpus in local dir
genStr = ''
while genStr is '':
    genStr = gen(f)

print "%s" % genStr

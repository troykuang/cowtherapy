import nltk
import string
import cowsay
import re
import random
from Grammar import *
from RB import *

test_bank=["I must do well in this exam", 
            "I am a worthless person", 
            "I must be accepted by people who I find important",
            "I am a bad person",
            "I must be approved by my friends"]

chatbot_prompts = [
   "Hi! I'm your self help chatbot. What is troubling you? ",
   "Hey! I'm your self help chatbot. How are you feeling? ",
   "How's it going? It's nice to see you again. What's on your mind? ",
   "There you are! I'm your self help chatbot. How are things? ",
   "Hi there! I'm your self help chatbot. How is it going? "
]

parser = nltk.ChartParser(rebt_grammar)

# Remove all the:
# 1) punctuations 
# 2) leading and trailing white spaces
# 3) turn the entire sting into lower case
def simplifyStr(inStr):
   return inStr.translate(str.maketrans('','',string.punctuation)).strip().lower()

def constructSentence(inStr, flag):
   base = inStr.capitalize()
   ret = base.replace(" i ", " I ")
   ret = ret.replace("-", " ")
   if flag == 'Q':
      ret += "?"
   elif flag == 'S':
      ret += "."
   return ret

# To check a sentence whether is in a passive voice or 
# an active voice using regular expression
# Regex used "(^.*)((be\s)([a-z]+ed))(.*$)"
# Group 1: anything before be
# Group 3: be and a \s
# Group 4: verb + pst
# Group 5: everything after the be v-ed
# Group 3 will be replaced with a "be-"
def unifyVoice(inStr):
   regex = r"(^.*)((be\s)([a-z]+ed))(.*$)"
   ret = re.sub(regex, r"\1be-\4\5", inStr)
   #print("the new setence is: " + ret)
   return ret

def unifyStr(inStr):
   ret = simplifyStr(inStr)
   ret = unifyVoice(ret)
   return ret

# Generate the parse tree(s)
def parserStr(inStr):
   trees = list(parser.parse(inStr.split(" ")))
   if (len(trees) == 0):
      raise Exception('Not able to generate a parse tree.')
   #printAllTrees(trees)
   #printTerminals(trees[0])
   return populatePOS(trees[0])

# Print out all the parse trees
def printAllTrees(trees):
   for t in trees:
      print(t)

# Print out parsed terminals of one parse tree
def printTerminals(tree):
   for s in tree.subtrees(lambda t: t.height() == 2):
      print(s)

# Get Parts of Speech (N, I, V, Adv, etc)
def populatePOS(tree):
   pos = {}
   for s in tree.subtrees(lambda t: t.height() == 2):
      if not (pos.get(s.label())):
         pos[s.label()] = []
      pos[s.label()].append(s.leaves()[0])
   #print(pos)
   return pos

# Return a list of terminals of one specific part of speech
def getPOS(hashmap, pos):
   return hashmap[pos][0]

def pickFromList(ls):
   l = len(ls)
   return ls[random.randint(0,l-1)]

# Take in POS of an irrational beliefs (IBs) as a dictionary
# Construct a sentence (Phase 1)/a list of sentences (Phase 2) of disputes 
# Return the sentence (Phase 1)/ a sentence from a list of disputes (Phase 2)
# How to construct a dispute:
# Two types of IB structure we are handling right now based on the existence of IP
# 1) Active voice: N I V A (NP): I must do well (in the exam)
#    Passive voice: N I PassiveV (NP): i must be accepted (by people)
# 2) N V A/N: I am awful
# Disputes:
# 1) Active voice: CP (Why) + I + N + V + A: Why must i do well
#    Passive voice: CP (Why) + I + N + PassiveV: Why must i be accepted
# 2) CP (Why) + V + N + A: Why is it/am i awful
def constructDisputes(hashmap):
   print("Formulating disputes implores you to try to find evidence to support your beliefs. Why do you feel a certain way, is there any evidence to support the feelings you have in this situation? By turning your beliefs into questions, we can further differentiate between irrational and rational beliefs. \n\n")

   CP = ''

   AP = ''
   if hashmap.get('Adv'):
      AP = getPOS(hashmap, 'Adv')
   elif hashmap.get('Adj'):
      AP = getPOS(hashmap, 'Adj')
   
   NP = getPOS(hashmap, 'N')
   
   if hashmap.get('I'):
      CP = 'why'
      # Active: CP + I + N + V + A
      # Passive CP + I + N + PassiveV: Why
      IP = getPOS(hashmap, 'I')
      VP = ''
      if hashmap.get('PassiveV'):
         VP = getPOS(hashmap, 'PassiveV')
         ret = CP + ' ' + IP + ' '  + NP + ' '  + VP
      elif hashmap.get('V'):
         VP = getPOS(hashmap, 'V')
         ret = CP + ' ' + IP + ' '  + NP + ' '  + VP + ' '  + AP
   else:
      CP = 'where is it written that'
      # Second struct: CP (Why) + VP + NP + AP
      VP = getPOS(hashmap, 'V')
      # Simple: Why am i bad?
      # ret = CP + ' ' + VP + ' '  + NP + ' '  + AP
      # More natural: where is it written that N + V + AP (I am awful)
      ret = CP + ' ' + NP + ' ' + VP + ' ' + AP
   return constructSentence(ret,'Q')

# Similar to constructDisputes, two types of RBs based on the existence of IP
def constructRBs(hashmap, ori):
   ret = ''
   print("IB: " + ori)
   if hashmap.get('I'):
      #print("I exists")
      IP = hashmap.get('I')
      replacementList = rbs[IP[0]]
      rationalI = pickFromList(replacementList)
      #print(replacementList)
      #print(rationalI)
      rbBase = ori.replace(IP[0], rationalI)
      ret = constructSentence(rbBase, 'S') + ' ' + pickFromList(typeA_RBs)
   else:
      # NP + VP + AdjP
      base = "There is no evidence that I am"
      Adj = hashmap.get('Adj')
      ret = base + ' ' + Adj[0] + '. '
      aux = pickFromList(typeB_RBs)
      if len(aux) > 0:
         ret +=  aux + Adj[0] + "ly."
   print("RB: " + ret)
   return ret

def init():
   print("Welcome to your self help chatbot.")
   print("The REBT (Rational Emotive Behaviour Therapy) chatbot is here to help turn irrational beliefs into rational beliefs.")
   print("\n\n")

def processInput(input):
      # Need to handle the case where the user input something invalid
      print("\n\n")
      
      print("Input string: ", input)
      send = unifyStr(input)
      hashmapPOS = parserStr(send)


      print("\n\n")
      print("Then we need to formulate the disputes for the belief...\n\n")
      dispute = constructDisputes(hashmapPOS)
   
      cowsay.cow(dispute)

      print("\n\n")
      print("Now we need to generate the rational belief...\n\n")
      rb = constructRBs(hashmapPOS, send)
      
      cowsay.cow(rb)


def main():
   # A dictionary that store various parts of speech of one sentence
   #hashmapPOS = {}
   init()

   prompt = 0
   promptMax = len(chatbot_prompts)
   
   cowsay.cow(chatbot_prompts[prompt])
   ipt = input("Enter your beliefs (one sentence at a time) leading up to the emotional disturbance or self-defeating behaviour.\nIf you no longer want to chat with me just input 'q' (quit). \n")

   # until the user wants to quit, it prompts for their IBs
   while ipt != "q":

      prompt = (prompt + 1) % promptMax
 
      # surrounded with try/except in case input is not handled (different than ones we accounted for)
      try:
         processInput(ipt)
         cowsay.cow(chatbot_prompts[prompt])

      except:
         cowsay.cow("Sorry, I didn't catch that.. maybe you can try to tell me a different way?")

      ipt = input("Enter your beliefs (one sentence at a time) leading up to the emotional disturbance or self-defeating behaviour.\nIf you no longer want to chat with me just input 'q' (quit). \n")

      
   
   # RBs
   # A dict of words: {'Must': ['prefer', 'would like to']}

main()

# Testing without the chatbot
# for inStr in test_bank:
#    send = unifyStr(inStr)
#    hashmapPOS = parserStr(send)
   
#    print("=====================")
#    #print(constructDisputes(hashmapPOS))
#    constructRBs(hashmapPOS, send)
#    print("=====================")
#    #print(hashmapPOS)


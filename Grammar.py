import nltk

# Terminal symbols are all in lower case

rebt_grammar = nltk.CFG.fromstring("""
IP -> NP IBar
IBar -> I VP | VP
NP -> Det NBar | NBar | N NBar
NBar -> AdjP NBar | NBar PP | N PP | N | N CP
AdjP -> AdvP AdjBar | AdjBar
AdjBar -> Adj | Adj PP
PP -> PBar | AdvP PBar
PBar -> P NP
VP -> VBar |V VBar
VBar -> V NP | V | AdvP VBar | VBar AdvP | V AdjP | VBar PP | V NP NP | V CP | PassiveV
AdvP -> AdvBar | AdvP AdvBar
AdvBar -> Adv
CP -> CBar
CBar -> C IP | IP

Adv -> 'really' | 'fully' | 'very' | 'well'
Adj -> 'important' | 'bad' | 'worthless' | 'unlovable' | 'awful' | 'horrible'
Det -> 'my' | 'this' | 'a'
N -> 'exam' | 'book' | 'people' | 'i' | 'person' | 'someone' | 'it' | 'friends'
I -> '-pst' | '+pst' | 'cannot' | 'cant' | 'haveto' | 'needto' | 'must' 
V -> 'do' | 'find' |  | 'be' | 'am'  | 'stand'
PassiveV -> 'be-approved' | 'be-accepted' | 'be-loved'
P -> 'in' | 'by'
C -> 'that' | 'who' | 'when'
""")
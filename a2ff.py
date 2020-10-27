'''a2ff.py
by Nuo Chen and Jack Lin
UWNetIDs: chenn24, xlin7799
Student numbers: 1765107, and 1765328

Assignment 2, in CSE 473, Autumn 2020.

Part A
 
This file contains our problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in 
# the format shown.

#<METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Farmer-Fox-Chicken-Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Nuo Chen', 'Jack Lin']
PROBLEM_CREATION_DATE = "27-OCT-2020"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The <b>"Farmer-Fox-Chicken-Grain"</b> problem is a traditional puzzle
A farmer has to get a fox, a chicken, and a sack of corn across a river.
He has a rowboat, and it can only carry him and one other thing.
If the fox and the chicken are left together, the fox will eat the chicken.
If the chicken and the corn are left together, the chicken will eat the corn.
How does the farmer do it?
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
FAMILY = ["Fox", "Chicken", "Grain", "Farmer"] # array that helps output textual description of a state
F = 0   # array index to check if Fox is there
C = 1   # array index to check if Chicken is there
G = 2   # array index to check if Grain is there
FA = 3  # Cross the river himself (Farmer)
LEFT = 0  # same idea for left side of river
RIGHT = 1 # same idea for right side of river

class State():

  def __init__(self, d=None):
    if d==None:
      d = {'farm':[[1, 1, 1],[0, 0, 0]], # 1 means the member is there and 0 is not
           'boat':LEFT}
    self.d = d

  def __eq__(self,s2):
    for prop in ['farm', 'boat']:
      if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    farm = self.d['farm']
    txt = "\n Here are members on left: "
    for i in range(len(farm[LEFT])):
      if farm[LEFT][i] == 1:
        txt += FAMILY[i] + " "
    txt += "\n"
    txt += " Here are members on right: "
    for i in range(len(farm[RIGHT])):
      if farm[RIGHT][i] == 1:
        txt += FAMILY[i] + " "
    txt += "\n"
    side='left'
    if self.d['boat']==1: side='right'
    txt += " boat and farmer are on the "+side+".\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.d['farm']=[self.d['farm'][LEFT_or_RIGHT][:] for LEFT_or_RIGHT in [LEFT, RIGHT]]
    news.d['boat'] = self.d['boat']
    return news

  def can_move(self,m):
    '''Tests whether it's legal to move the boat and take
     m missionaries and c cannibals.'''
    side = self.d['boat'] # Where the boat and farmer is.
    farm = self.d['farm']
    if m != FA: # Cross river with a member on the boat
      if farm[side][m] == 0: return False # m is not here
      if m == F and farm[side][C] == 1 and farm[side][G] == 1: return False # Chicken and Grain at the same side
      if m == G and farm[side][C] == 1 and farm[side][F] == 1: return False # Chicken and Fox at the same side
    else: # Cross river himself (farmer)
      if farm[side][C] == 1 and farm[side][G] == 1: return False # Chicken and Grain at the same side
      if farm[side][C] == 1 and farm[side][F] == 1: return False # Chicken and Fox at the same side
    return True

  def move(self,m):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the boat carrying
     m missionaries and c cannibals.'''
    news = self.copy()      # start with a deep copy.
    side = self.d['boat']   # where is the boat?
    farm = news.d['farm']   # get the current state
    if m == FA: # Cross river himself (farmer), then Move the boat itself.
      news.d['boat'] = 1 - side
      return news
    # Cross river with a member on the boat
    farm[side][m] = 0             # Remove the member from current side
    farm[1 - side][m] = 1         # Add the member to the other side
    news.d['boat'] = 1-side       # Move the boat itself.
    return news

def goal_test(s):
  farm = s.d['farm']
  return farm[RIGHT][F] == 1 and farm[RIGHT][C] == 1 and farm[RIGHT][G] == 1 # all members come to the right side

def goal_message(s):
  return "Congratulations on successfully guiding Fox, Chicken, and Grain across the river!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'farm':[[1, 1, 1], [0, 0, 0]], 'boat':LEFT })
#</INITIAL_STATE>

#<OPERATORS>

OPERATORS = [Operator(
  "Cross the river with "+ FAMILY[m],
  lambda s, m1=m: s.can_move(m1),
  lambda s, m1=m: s.move(m1))
  for m in [F, C, G, FA]]

#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>






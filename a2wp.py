'''a2wp.py
by Nuo Chen and Jack Lin
UWNetIDs: chenn24, xlin7799
Student numbers: 1765107, and 1765328

Assignment 2, in CSE 473, Autumn 2020.
PART B

This file contains our problem formulation for the problem of
reducing plastic waste.
'''

# Put your formulation of your chosen wicked problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in
# the format shown.

#<METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Reducing Plastic Waste"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Nuo Chen', 'Jack Lin']
PROBLEM_CREATION_DATE = "27-Oct-2020"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The <b>"Plastic waste"</b> problem has long been a global concern. Plastic waste can be 
 detrimental to our environment because it is hard to degrade and takes up to 400 years to
 decompose naturally. We therefore come up with a mathmatical model that simulates the amount
 of plastic waste produced each year, in terms of the market demand and amount of recycling, in
 response to different regulatory policies. 

Underlying principles:
1) new waste produced = market demand of plastic - plastic recycled from last year
2) plastic recycled = recycling rate * new plastic waste produced last year, since most of the
   plastic can only be recycled once
3) market demand of plastic = demand rate * DEMAND_CONSTANT

Mathematical formula:
W(t) = d*DEMAND_CONSTANT - r*W(t-1)
1) W(t): new platic waste produced at year t
2) d: demand factor, total demand is a fraction of DEMAND_CONSTANT
3) r: recycling factor
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
DEMAND_CONSTANT = 381 # plastic demand in million tonnes
RECYCLE_COST = 20     # Investment in Research for better recycling technology
ADS_COST = 10         # Investment in educational propaganda that disencourages plastic consumption
class State():

  def __init__(self, d=None):
    if d == None:
      d = {'year': 0,
           'prev_recycled': 0,
           'd': 0,
           'r': 0,
           'new_waste': 0,
           'fund': 0}
    self.d = d

  def __eq__(self,s2):
    for prop in ['year', 'prev_recycled', 'd', 'r', 'new_waste', 'fund']:
      if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    txt = "\n Year: " + str(self.d['year']) + "\n"
    txt += " Total platic demand: " + str(self.d['d'] * DEMAND_CONSTANT) + " million tonnes\n"
    txt += " Plastic recycled from previous year: " + str(self.d['prev_recycled']) + "\n"
    txt += " Recycling rate: " + str(self.d['r']) + "\n"
    txt += " New plastic waste: " + str(self.d['new_waste']) + " million tonnes\n"
    txt += " Current fund remaining: $" + str(self.d['fund']) + " million\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.d['year'] = self.d['year']
    news.d['prev_recycled'] = self.d['prev_recycled']
    news.d['d'] = self.d['d']
    news.d['r'] = self.d['r']
    news.d['new_waste'] = self.d['new_waste']
    news.d['fund'] = self.d['fund']
    return news

  def update_waste(self):
    # computes the new waste generated
    self.d['new_waste'] = self.d['d'] * DEMAND_CONSTANT - self.d['prev_recycled']

  def check_fund(self, exp):
    # checks if current fund >= exp (expenditure)
    if self.d['fund'] >= exp:
      return True
    return False

  def f_Recycle(self):
    # print('Investing in Research for better recycling technology')
    news = self.copy()
    news.d['year'] += 1
    news.d['fund'] -= RECYCLE_COST
    news.d['r'] *= 1.4
    news.d['prev_recycled'] = news.d['new_waste'] * news.d['r']
    news.update_waste()
    return news

  def f_Ads(self):
    # print('Investing in educational propaganda that disencourages plastic consumption')
    news = self.copy()
    news.d['year'] += 1
    news.d['fund'] -= ADS_COST
    news.d['d'] *= 0.7
    news.d['prev_recycled'] = news.d['new_waste'] * news.d['r']
    news.update_waste()
    return news

  def f_Skip(self):
    # print('Doing nothing this year because of insufficient fund')
    news = self.copy()
    news.d['year'] += 1
    news.d['fund'] += 50
    news.d['d'] = min(1, news.d['d']*1.1) # natural growth of demand
    news.d['prev_recycled'] = news.d['new_waste'] * news.d['r']
    news.update_waste()
    return news

def goal_test(s):
  return s.d['new_waste'] <= 100

def goal_message(s):
  return "Thanks for your effort! This year, there is less than 100 million tonnes of platic waste produced."

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
CREATE_INITIAL_STATE = lambda : State(d={'year':2020,
           'prev_recycled':73,
           'd':1.0,
           'r':0.2,
           'new_waste':308,
           'fund':100})
#</INITIAL_STATE>

#<OPERATORS>

op1 = Operator(
  "Invest $"+str(RECYCLE_COST)+" million in developing better recycling technology" ,
  lambda s: s.check_fund(RECYCLE_COST),
  lambda s: s.f_Recycle())

op2 = Operator(
  "Invest $"+str(ADS_COST)+" million in distributing educational propaganda" ,
  lambda s: s.check_fund(ADS_COST),
  lambda s: s.f_Ads())

op3 = Operator(
  "Do nothing to raise more fund ($50 millions)" ,
  lambda s: s.check_fund(0),
  lambda s: s.f_Skip())

OPERATORS = [op1, op2, op3]

#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

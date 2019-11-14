# -*- coding: utf-8 -*-
import re
import sys
import logic
import planning
import search
from utils import (remove_all, unique, first, argmax, probability, isnumber,
                   issequence, Expr, expr, subexpressions, extend)

""" A2 Part A

    giveFeedback is a function that reads in a student state and returns a feedback message using propositional logic and proof by resolution. The rules
    for how to decide which message to return are given in the assignment description.
    
    studentState:   a String representing a conjunction of five possible symbols: CorrectAnswer, NewSkill, MasteredSkill, CorrectStreak, IncorrectStreak
                    For example, you could call giveFeedback('CorrectAnswer') or giveFeedback('MasteredSkill & CorrectStreak')
    
    feedbackMessage:a String representing one of eight feedback messages (M1 through M8 below). 
    
    Feel free to refactor the code to move M1 through M8 into a class, but the function call and return values should remain as specified below for our grading.
"""
C = expr("CorrectAnswer")
M = expr("MasteredSkill")
B = expr("IsBored")
CS = expr("CorrectStreak")
IS = expr("IncorrectStreak")
N = expr("NewSkill")
E = expr("NeedsEncouragement")


M1 = 'Correct. Keep up the good work!'
M2 = 'Correct. I think you’re getting it!'
M3 = 'Correct. After this problem we can switch to a new problem.'
M4 = 'Incorrect. Keep trying and I’m sure you’ll get it!'
M5 = 'Incorrect. After this problem, we can switch to a new activity.'
M6 = 'Incorrect. The following is the correct answer to the problem.'
M7 = 'Correct.'
M8 = 'Incorrect.'
dictionary = {1: M1, 2: M2, 3: M3, 4: M4, 5: M5, 6: M6, 7: M7, 8: M8}


def giveFeedback(studentState):
    # Add the rules of feedback system
    feedbackkb = logic.PropKB()
    feedbackkb.tell(C | '==>' | (expr('M1') | expr('M2') | expr('M3') | expr('M7')))
    feedbackkb.tell(~C | '==>' | (expr('M4') | expr('M5') | expr('M6') | expr('M8')))
    feedbackkb.tell(((M & ~C) | (M & CS)) | '==>' | B)
    feedbackkb.tell((N | IS) | '==>' | expr('M6'))
    feedbackkb.tell(((IS & C) | (N & CS)) | '==>' | E)
    feedbackkb.tell(E | '==>' | (expr('M2') | expr('M4')))
    feedbackkb.tell(B | '==>' | (expr('M3') | expr('M5')))
    feedbackkb.tell(((N & C) | CS) | '==>' | expr('M1'))

    # Add student state
    feedbackkb.tell(studentState)

    # Iteratively Add ~M1, ~M2, .... ~M8 to knowledge base whenever a resolution returns false
    for i in range(1, 9):
        msg = 'M' + str(i)
        if i == 2:
            feedbackkb.tell(expr('~M4'))
        if logic.pl_resolution(feedbackkb, expr(msg)):  # If entailment happens, return that message
            return dictionary[i]

        if i == 2:
            feedbackkb.retract(expr('~M4'))
        feedbackkb.tell(expr('~' + msg))  # Can add to knowledge base since we know can't be this particular msg

    return None

    
""" A2 Part B

    solveEquation is a function that converts a string representation of an equation to a first-order logic representation, and then
    uses a forward planning algorithm to solve the equation. 
    
    equation:   a String representing the equation to be solved. "x=3", "-3x=6", "3x-2=6", "4+3x=6x-7" are all possible Strings.
                For example, you could call solveEquation('x=6') or solveEquation('-3x=6')
    
    plan:   return a list of Strings, where each String is a step in the plan. The Strings should reference the core actions described in the
            Task Domain part of the assignment description.
    
"""
SAMPLE_EQUATION = '3x-2=6'
SAMPLE_ACTION_PLAN = ['add 2', 'combine RHS constant terms', 'divide 3']

action1 = planning.Action('CombineLeftConstants(a, b)',
                            precond='LHC(a) & LHC(b)',
                            effect='~LHC(b)')
action2 = planning.Action('CombineRightConstants(a, b)',
                            precond='RHC(a) & RHC(b)',
                            effect='~RHC(a) & ~RHC(b) & RHC({0})'.format(-sys.maxsize))
action3 = planning.Action('CombineLeftVariables(a, b)',
                            precond='LHV(a) & LHV(b)',
                            effect='~LHV(a) & ~LHV(b) & LHV({0})'.format(-sys.maxsize))
action4 = planning.Action('CombineRightVariables(a, b)',
                            precond='RHV(a) & RHV(b)',
                            effect='~RHV(a)')
action5 = planning.Action('AddVariable(b)',
                            precond='RHV(b)',
                            effect='~RHV(b) & LHV(b)')
action6 = planning.Action('AddConstant(a)',
                            precond='LHC(a)',
                            effect='~LHC(a) & RHC(a)')
action7 = planning.Action('Divide()',
                            precond='LHV({0}) & RHC({0})'.format(-sys.maxsize),
                            effect='LHV({1}) & ~LHV({0}) & RHC({1}) & ~RHC({0})'.format(-sys.maxsize, -sys.maxsize - 1))


def solveEquation(equation):
    sides = equation.split('=')     # Initial parsing of equation
    for i in range(0, len(sides)):
        minuslocs = reversed([pos for pos, char in enumerate(sides[i]) if char == '-'])
        for loc in minuslocs:
            if loc != 0:
                sides[i] = sides[i][0:loc] + "+" + sides[i][loc:]
    left = sides[0].split('+')
    right = sides[1].split('+')

    initial = ''  # Creating initial clauses
    for term in left:
        if term.find('x') != -1:
            if term == 'x':
                initial += 'LHV(1) & '
            elif term == '-x':
                initial += 'LHV(-1) & '
            else:
                initial += 'LHV(' + term[0:len(term) - 1] + ') & '
        else:
            initial += 'LHC(' + term + ') & '
    for term in right:
        if term.find('x') != -1:
            if term == 'x':
                initial += 'RHV(1) & '
            elif term == '-x':
                initial += 'RHV(-1) & '
            else:
                initial += 'RHV(' + term[0:len(term) - 1] + ') & '
        else:
            initial += 'RHC(' + term + ') & '
    if initial.count('LHV') == 1 and initial.find('RHV') == -1:
        initial += 'LHV(0) & '
    if initial.count('RHC') == 1 and initial.find('LHC') == -1:
        initial += 'RHC(0) & '
    if initial.find('LHV') == -1:
        initial += 'LHV(0) & '
    if initial.find('RHC') == -1:
        initial += 'RHC(0) & '
    initial = initial[: len(initial) - 3]

    goal = 'LHV({0}) & RHC({0})'.format(-sys.maxsize - 1)    # Specifying goal state
    actions = [action1, action2, action3, action4, action5, action6, action7]

    problem = planning.PlanningProblem(initial, goal, actions)
    forward_planning = planning.ForwardPlan(problem)
    plan = search.astar_search(forward_planning)

    action_plan = []
    while plan.parent is not None:
        step = plan.action
        if 0 not in step.args:
            action_plan.insert(0, plan.action)
        plan = plan.parent

    action_plan = parseActionPlan(action_plan, initial)

    return action_plan


def parseActionPlan(action_plan, vars):
    interLeftC = 0
    interLeftV = 0
    interRightC = 0
    interRightV = 0
    for i in range(0, len(action_plan)):
        action = action_plan[i]
        if action.name == 'AddConstant':
            if interLeftC == 0:
                interRightC = -1 * action.args[0]
            else:
                interRightC = -1 * interLeftC
            interLeftC = 0
            action_plan[i] = 'add ' + str(interRightC)
        elif action.name == 'AddVariable':
            if interRightV == 0:
                interLeftV = -1 * action.args[0]
            else:
                interLeftV = -1 * interRightV
            interRightV = 0
            action_plan[i] = 'add ' + str(interLeftV) + 'x'
        elif action.name == 'CombineRightConstants':
            action_plan[i] = 'Combine RHS constants'
            interRightC += action.args[0] + action.args[1]
        elif action.name == 'CombineLeftConstants':
            action_plan[i] = 'Combine LHS constants'
            interLeftC += action.args[0] + action.args[1]
        elif action.name == 'CombineRightVariables':
            action_plan[i] = 'Combine RHS constants'
            interRightV += action.args[0] + action.args[1]
        elif action.name == 'CombineLeftVariables':
            action_plan[i] = 'Combine LHS constants'
            interLeftV += action.args[0] + action.args[1]
        else:
            left = [m.start() for m in re.finditer('LHV', vars)]
            right = [m.start() for m in re.finditer('RHV', vars)]
            coeff = 0
            for index in left:
                index = index + 4
                try:
                    coeff += int(vars[index: index + 1])
                except ValueError:
                    coeff += int(vars[index: index + 2])
            for index in right:
                index = index + 4
                try:
                    coeff += -1 * int(vars[index: index + 1])
                except ValueError:
                    coeff += -1 * int(vars[index: index + 2])
            if coeff == 1:
                del action_plan[i]
            else:
                action_plan[i] = 'divide ' + str(coeff)

    return action_plan


""" A2 Part C

    predictSuccess is a function that takes in a list of skills students have and an equation to be solved, and returns the skills
    students need but do not currently have in order to solve the skill. For example, if students are solving the problem 3x+2=8, and have S7 and S8, 
    they would still need S4 and S5 to solve the problem.
    
    current_skills: A list of skills students currently have, represented by S1 through S9 (described in the assignment description)
    
    equation:   a String representing the equation to be solved. "x=3", "-3x=6", "3x-2=6", "4+3x=6x-7" are all possible Strings.
                For example, you could call solveEquation('x=6') or solveEquation('-3x=6')
    
    missing_skills: A list of skills students need to solve the problem, represented by S1 through S9.
    
"""
CURRENT_SKILLS = ['S8','S9']
EQUATION = '3x+2=8'
SAMPLE_MISSING_SKILLS = ['S4','S5']

def predictSuccess(current_skills, equation):
    missing_skills = SAMPLE_MISSING_SKILLS
    return missing_skills

   
""" A2 Part D

    stepThroughProblem is a function that takes a problem, a student action, and a list of current student skills, and returns
    a list containing a feedback message to the student and their updated list of skills.
    
    equation: a String representing the equation to be solved. "x=3", "-3x=6", "3x-2=6", "4+3x=6x-7" are all possible Strings.
    
    action: an action in the task domain. For example: 'add 2', 'combine RHS constant terms', 'divide 3'
    
    current_skills: A list of skills students currently have, represented by S1 through S9 (described in the assignment description)
    
    feedback_message: A feedback message chosen correctly from M1-M9.
    
    updated_skills: A list of skills students have after executing the action.
    
"""
CURRENT_SKILLS = ['S8','S9']
EQUATION = '3x+2=8'
ACTION = 'add -2'
UPDATED_SKILLS = ['S8','S9','S4']


def stepThroughProblem(equation, action, current_skills):
    feedback_message = M1
    updated_skills = UPDATED_SKILLS
    return [feedback_message,updated_skills]


if __name__ == '__main__':
    # feedback = giveFeedback("CorrectAnswer")
    # print(feedback)
    # eqn = solveEquation('x=2')
    # print(eqn)
    # eqn = solveEquation('-3x=6')
    # print(eqn)
    # eqn = solveEquation('3x-2=-6')
    # print(eqn)

    eqn = solveEquation('3x+x=-6x-4')
    print(eqn)
    eqn = solveEquation('2x+3=2+4')
    print(eqn)

    # eqn = solveEquation('2=x')
    # print(eqn)
    # eqn = solveEquation('6=-3x')
    # print(eqn)
    # eqn = solveEquation('-6=3x-2')
    # print(eqn)
    # eqn = solveEquation('-6x-4=3x+x')
    # print(eqn)
    # eqn = solveEquation('2+4=2x+3')
    # print(eqn)
    # eqn = solveEquation('x+2x=2+4')
    # print(eqn)
    # eqn = solveEquation('x+2=2x+4')
    # print(eqn)
    # eqn = solveEquation('2+4=x+2x')
    # print(eqn)

                                
                             


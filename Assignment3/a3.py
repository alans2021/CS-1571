from tree import Utility
from tree import Choice
from tree import Decision
from probability import BayesNet
from probability import enumeration_ask


# First create all nodes with connections and probabilities. Then find the value of first decision node
# Does expectimax algorithm do determine action that D1 node should take
def q2():

    # Create all utility nodes first
    U1 = Utility(.1, 100, 'Resolved')
    U2 = Utility(.3, 5, 'Frustrated')
    U3 = Utility(.7, -95, '~Frustrated')
    U4 = Utility(.9, 0, '~Resolved')
    U5 = Utility(.1, 100, 'Resolved')
    U6 = Utility(.3, 10, 'Frustrated')
    U7 = Utility(.7, -90, '~Frustrated')

    # Then create all choice nodes with connections to utilities
    C2 = Choice('Redirect')
    C2.addChildren(U2)
    C2.addChildren(U3)

    C4 = Choice('Redirect')
    C4.addChildren(U6)
    C4.addChildren(U7)

    C3 = Choice('Respond')
    C3.addChildren(U4)
    C3.addChildren(U5)

    C1 = Choice('Respond')
    C1.addChildren(U1)

    # Create decision nodes
    D2 = Decision(0.9, '~Resolved')
    D2.addChildren(C3)
    D2.addChildren(C4)
    C1.addChildren(D2)

    D1 = Decision()
    D1.addChildren(C1)
    D1.addChildren(C2)

    return 'Value for D1 is ' + str(D1.value()) + ' and ' + 'Action from D1 is ' + D1.action


def q6(variable, conditions, value):
    T, F = True, False
    chatbot = BayesNet([
        ('Accurate', '', 0.9),
        ('ProblemSize', '', 0.9),   # 0.9 is probabililty that problem size is small
        ('ConversationLength', 'ProblemSize', {T: (0.40, 0.40, 0.20), F: (0.20, 0.30, 0.50)}, 3),
        ('Frustrated', 'Accurate ProblemSize ConversationLength',
         {(T, T, 0): 0.20, (T, T, 1): 0.30, (T, T, 2): 0.60,
          (T, F, 0): 0.30, (T, F, 1): 0.60, (T, F, 2): 0.70,
          (F, T, 0): 0.40, (F, T, 1): 0.50, (F, T, 2): 0.80,
          (F, F, 0): 0.50, (F, F, 1): 0.80, (F, F, 2): 0.90}),
        ('Resolved', 'Accurate ConversationLength',
         {(T, 0): 0.30, (T, 1): 0.50, (T, 2): 0.70,
          (F, 0): 0.20, (F, 1): 0.30, (F, 2): 0.40})
    ])

    probdist = enumeration_ask(variable, conditions, chatbot)

    psize_dict = {True: 'Small', False: 'Big'}
    clength_dict = {0: 'Short', 1: 'Medium', 2: 'Long'}
    for var in conditions:
        if var == 'ProblemSize':
            conditions[var] = psize_dict[conditions[var]]
        if var == 'ConversationLength':
            conditions[var] = clength_dict[conditions[var]]

    return 'Probability of ' + variable + ' being ' + str(value) + ' given ' + \
           str(conditions) + ': ' + str(probdist.prob[value])


if __name__ == '__main__':
    answer = q2()
    print(answer)

    a = q6('ConversationLength', dict(ProblemSize=True), 0)
    print(a)

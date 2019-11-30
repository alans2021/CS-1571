from tree import Utility
from tree import Choice
from tree import Decision
from probability import BayesNet
from probability import enumeration_ask
from probability import BayesNode


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
psize_dict = {True: 'Small', False: 'Big'}
clength_dict = {0: 'Short', 1: 'Medium', 2: 'Long'}


def q8(variable, conditions, value):

    # Do enumeration ask
    probdist = enumeration_ask(variable, conditions, chatbot)

    # Parse input to output in correct format

    for var in conditions:
        if var == 'ProblemSize':
            conditions[var] = psize_dict[conditions[var]]
        if var == 'ConversationLength':
            conditions[var] = clength_dict[conditions[var]]
    prob = round(probdist.prob[value], 4)

    if type(value) == int:
        value = clength_dict[value]

    return 'Probability of ' + variable + ' being ' + str(value) + ' given ' + \
           str(conditions) + ': ' + str(prob)


def q9():
    # Full joint distribution of bayes net
    print('Full Joint Distribution of Bayes Net:')
    accurate = [True, False]
    psize = [True, False]
    clength = [0, 1, 2]
    resolved = [True, False]
    frustrated = [True, False]

    nodea = chatbot.variable_node('Accurate')
    nodep = chatbot.variable_node('ProblemSize')
    nodec = chatbot.variable_node('ConversationLength')
    noder = chatbot.variable_node('Resolved')
    nodef = chatbot.variable_node('Frustrated')

    for a in accurate:
        proba = nodea.p(a, {})
        for p in psize:
            probp = nodep.p(p, {})
            for c in clength:
                probc = nodec.p(c, {'ProblemSize': p})
                for r in resolved:
                    probr = noder.p(r, {'ConversationLength': c, 'Accurate': a})
                    for f in frustrated:
                        probf = nodef.p(f, {'ProblemSize': p, 'ConversationLength': c, 'Accurate': a})
                        finalprob = round(proba * probp * probc * probr * probf, 6)
                        print('Probability when Accuracy = ' + str(a) + ', Problem_Size = ' + psize_dict[p] +
                              ', Conversation_Length = ' + clength_dict[c] + ', Resolved = ' + str(r) +
                              ', Frustrated = ' + str(f) + ': ' + str(finalprob))


if __name__ == '__main__':
    # answer = q2()
    # print(answer)
    #
    a = q8('Resolved', dict(ProblemSize=True), True)
    print(a)
    q9()

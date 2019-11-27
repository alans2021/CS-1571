from tree import Utility
from tree import Choice
from tree import Decision


# First create all nodes with connections and probabilities. Then find the value of first decision node
def q1():

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


if __name__ == '__main__':
    answer = q1()
    print(answer)


class Node:

    def __init__(self):
        self.parent = None
        self.children = []

    def setParent(self, p):
        self.parent = p

    def addChildren(self, c):
        self.children.append(c)
        c.setParent(self)

    def value(self):
        raise NotImplementedError


class Utility(Node):

    def __init__(self, p, u, d):
        super().__init__()
        self.probability = p
        self.utility = u
        self.description = d
        self.val = 0

    def value(self):
        self.val = self.probability * self.utility
        return self.val


class Choice(Node):

    def __init__(self, desc):
        super().__init__()
        self.description = desc
        self.val = 0

    def value(self):
        for child in self.children:
            self.val += child.value()
        return self.val


class Decision(Node):

    def __init__(self, p=1.0, desc=None):
        super().__init__()
        self.probability = p
        self.description = desc
        self.action = None
        self.val = 0

    def value(self):
        val1 = self.children[0].value()
        val2 = self.children[1].value()
        if val1 > val2:
            self.val = val1
            self.action = self.children[0].description
        else:
            self.val = val2
            self.action = self.children[1].description
        return self.val * self.probability

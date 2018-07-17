from abc import ABC, abstractmethod


class Node(ABC):

    @abstractmethod
    def evaluate(self):
        pass


class StringNode(Node):

    def __init__(self, value):
        self.value = str(value)

    def evaluate(self):
        return self.value

    def __repr__(self):
        return str(self.value)


class NumberNode(Node):
    def __init__(self, value):
        self.value = int(value)

    def evaluate(self):
        return int(self.value)

    def __add__(self, other):
        if type(other) == NumberNode:
            return NumberNode(self.value + other.value)
        elif type(other) == int:
            return self.value + other

    def __sub__(self, other):
        if type(other) == NumberNode:
            return self.value - other.value
        elif type(other) == int:
            return self.value - other

    def __mul__(self, other):
        if type(other) == NumberNode:
            return self.value * other.value
        elif type(other) == int:
            return self.value * other

    def __floordiv__(self, other):
        if type(other) == NumberNode:
            return self.value // other.value
        elif type(other) == int:
            return self.value // other

    def __truediv__(self, other):
        if type(other) == NumberNode:
            return self.value / other.value
        elif type(other) == int:
            return self.value / other

    def __mod__(self, other):
        if type(other) == NumberNode:
            return self.value % other.value
        elif type(other) == int:
            return self.value % other

    def __pow__(self, other):
        if type(other) == NumberNode:
            return self.value ** other.value
        elif type(other) == int:
            return self.value ** other

    def __lt__(self, other):
        if type(other) == NumberNode:
            return self.value < other.value
        elif type(other) == int:
            return self.value < other

    def __le__(self, other):
        if type(other) == NumberNode:
            return self.value <= other.value
        elif type(other) == int:
            return self.value <= other

    def __gt__(self, other):
        if type(other) == NumberNode:
            return self.value > other.value
        elif type(other) == int:
            return self.value > other

    def __ge__(self, other):
        if type(other) == NumberNode:
            return self.value >= other.value
        elif type(other) == int:
            return self.value >= other

    def __eq__(self, other):
        if type(other) == NumberNode:
            return self.value == other.value
        elif type(other) == int:
            return self.value == other

    def __ne__(self, other):
        if type(other) == NumberNode:
            return self.value != other.value
        elif type(other) == int:
            return self.value != other

    def __repr__(self):
        return str(self.value)


class InstructionSetNode(Node):

    def __init__():
        raise Exception('Not Implemented Yet')

    def evaluate(self):
        raise Exception('Not Implemented Yet')


class InstructionNode(Node):
    pass


class RTypeInstructionNode(InstructionNode):

    def __init__(self, instruction_name, rt, rs):
        print(f'rd, rt, rs : {instruction_name}, {rt}, {rs}')

    def evaluate(self):
        raise Exception()

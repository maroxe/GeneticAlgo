import operator
import random
import pydot

strategy = None

class Rule(object):
    name = 'Unamed rule'
    children = []
    parent = None
    
    def __init__(self):
        for c in self.children:
            c.parent = self
            
    def pydot(self, graph):
        map(lambda child: child.pydot(graph), self.children)
        self.node = str(id(self))
        graph.add_node(pydot.Node(self.node, label=self.name))
        map(lambda child: graph.add_edge(pydot.Edge(self.node, child.node)), self.children)

    def num_nodes(self):
        return 1 + sum([c.num_nodes() for c in self.children])
    
    def nodes(self):
        return reduce(operator.add,  [c.nodes() for c in self.children],  [self])
    
    def type(self):
        class_name = self.__class__
        return class_name
    
    def mutate_child(self, h_max):
        try:
            i = random.choice(range(len(self.children)))
            self.children[i] = self.children[i].generate(h_max)
            self.children[i].parent = self
        except IndexError:
            pass
        
    def replace_child(self, child_to_replace, new_child):
        i, _ = filter(lambda (i, c): c == child_to_replace, enumerate(self.children))[0]
        self.children[i] = new_child
        new_child.parent = self
        
    def __repr__(self):
        return self.name + '(%d)' % id(self) 
     
class BinaryRule(Rule):
    def __init__(self, children):
        self.children = children
        self.child1, self.child2 = self.children
        super(BinaryRule, self).__init__()
        
    def copy(self):
        children = [c.copy() for c in self.children]
        for c in children: c.parent = self
        return self.type()(children)
    
class UnaryRule(Rule):
    def __init__(self, child):
        self.children = [child]
        self.child = child
        super(UnaryRule, self).__init__()

    def copy(self):
        child = self.child.copy()
        child.parent = self
        return self.type()(child)
    
class Constante(Rule):
    def __init__(self, value):
        self.value = value
        self.name = str(value)
        super(Constante, self).__init__()
        
    def eval(self):
        return self.value
    
    def copy(self):
        return self.type()(self.value)
     
class ArithmeticRule(BinaryRule):
    @classmethod
    def generate(cls, h_max):
        return cls([generate_float(h_max-1), generate_float(h_max-1)])   
    
class LessThan(BinaryRule):
    name = '<'
    
    @staticmethod
    def generate(h_max):
        return LessThan([generate_float(h_max-1), generate_float(h_max-1)])
    
    def eval(self):
        return self.child1.eval() < self.child2.eval()

class And(BinaryRule):
    name = 'and'
    
    @staticmethod
    def generate(h_max):
        return And([generate_bool(h_max-1), generate_bool(h_max-1)])
    
    def eval(self):
        return self.child1.eval() and self.child2.eval()

class Or(BinaryRule):
    name = 'or'
    
    @staticmethod
    def generate(h_max):
        return Or([generate_bool(h_max-1), generate_bool(h_max-1)])
    
    def eval(self):
        return self.child1.eval() or self.child2.eval()

class Plus(ArithmeticRule):
    name = '+'
    
    def eval(self):
        return self.child1.eval() + self.child2.eval()

class Mult(ArithmeticRule):
    name = '*'
    
    def eval(self):
        return self.child1.eval() * self.child2.eval()
    
class SMA(UnaryRule):
    name = 'sma'
    
    @staticmethod
    def generate(h_max):
        return SMA(generate_int(h_max-1))
    
    def eval(self):
        return strategy.getSMA(self.child.eval())

class Max(UnaryRule):
    name = 'max'
    
    @staticmethod
    def generate(h_max):
        return SMA(generate_int(h_max-1))
    
    def eval(self):
        return strategy.getMax(self.child.eval())
    
class Float(Constante):

    @staticmethod
    def generate(h_max):
        return Float(random.random()*30)

class Int(Constante):

    @staticmethod
    def generate(h_max):
        return Float(random.randint(1, 30))
    
class Price(Constante):
    name = 'price'
     
    def __init__(self, value):
        super(Price, self).__init__(self.name)
    
    def eval(self):
        return strategy.getMax(1)
     
    @staticmethod
    def generate(h_max):
        return Price(0)
    
class Boolean(Constante):
    @staticmethod
    def generate(h_max):
        return Boolean(random.random() > 0.5)

def draw_tree(t, image):
    graph = pydot.Dot(graph_type='graph')
    t.pydot(graph)
    graph.write_png(image)
    
bool_rules = [LessThan, Or, And, Boolean]
non_trivial_bool_rules = [LessThan, Or, And]
float_rules = [Price, SMA, Max, Float, Plus, Mult]
integer_rules = [Int]

float_constantes = [Price, SMA, Max, Float]
integer_constantes = [Int]

def generate_bool(h_max):
    if h_max <= 1:
        return Boolean.generate(h_max-1)
    return random.choice(non_trivial_bool_rules).generate(h_max-1)

def generate_float(h_max):
    if h_max <= 1:
        return random.choice(float_constantes).generate(h_max-1)
    return random.choice(float_rules).generate(h_max-1)

def generate_int(h_max):
    return Int.generate(h_max-1)


    

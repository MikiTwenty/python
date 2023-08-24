from math import log, sqrt

def core(fuzzy_set):
    val = []
    for value in fuzzy_set:
        if fuzzy_set[value] == 1:
            val.append(value)
    print("Core: " + str(val))
    return val

def support(fuzzy_set):
    val = []
    for value in fuzzy_set:
        val.append(value)
    print("Support: " + str(val))
    return(val)

def cardinality(fuzzy_set, output=True):
    val = 0
    for membership in fuzzy_set.values():
        val += membership
    if output: print("Cardinality: " + "{:.2f}".format(val))
    return val

def acut(fuzzy_set, a):
    val = []
    for value in fuzzy_set:
        if fuzzy_set[value] > a:
            val.append(value)
    print("Alpha-cut(" + str(a) + "): " + str(val))
    return val

def owa(fuzzy_set, weights):
    if len(fuzzy_set) != len(weights):
        return ValueError
    else:
        val = 0
        values = sorted(fuzzy_set.values(), reverse=True)
        for n in len(values):
            val += values[n]*weights[n]
    print("Ordered weighted average: " + str(val))
    return val

def gravity_center(fuzzy_set):
    val = 0
    for value in fuzzy_set:
        val += float(value) * fuzzy_set[value]
    val /= cardinality(fuzzy_set, output=False)
    print("Center of gravity: " + "{:.2f}".format(val))
    return val

def entropy(fuzzy_set):
    val = 0
    for membership in fuzzy_set.values():
        if membership != 0 and membership != 1:
            val += -(membership * log(membership)) - ((1 - membership) * log(1 - membership))
    print("Entropy: " + "{:.2f}".format(val))
    return val

def fuzziness(fuzzy_set, distance="hamming"):
    if distance == "hamming":
        val = 0
        total_sum = sum(fuzzy_set.values())
        if total_sum != 0:
            for membership in fuzzy_set.values():
                if membership != 0:
                    val += abs(membership - (1 - membership))
            val = 1 - (val/len(fuzzy_set))
        print("Fuzziness (Hamming distance): " + "{:.2f}".format(val))
    elif distance == "euclidean":
        val = 0
        total_sum = sum(fuzzy_set.values())
        if total_sum != 0:
            for membership in fuzzy_set.values():
                if membership != 0:
                    val += (abs(membership - (1 - membership)))**2
            val = 1 - (sqrt(val)/len(fuzzy_set))
        print("Fuzziness (Euclidean distance): " + "{:.2f}".format(val))
    else:
        raise ValueError("Invalid distance type.")
    return val

def tnorm(a, b, tnorm_type="lukasiewicz"):
    if tnorm_type == "lukasiewicz":
        val = max(0, a + b - 1)
        print("Lukasiewicz t-norm("+ str(a) + ", " + str(b) + ")" + ": "  + "{:.2f}".format(val))
    elif tnorm_type == "godel":
        val = min(a, b)
        print("Godel t-norm("+ str(a) + ", " + str(b) + ")" + ": "  + "{:.2f}".format(val))
    elif tnorm_type == "product":
        val = a * b
        print("Product("+ str(a) + ", " + str(b) + ")" + ": "  + "{:.2f}".format(val))
    elif tnorm_type == "drastic":
        if a == 1:
            val = b
        elif b == 1:
            val = a
        else:
            val = 0
        print("Drastic t-norm("+ str(a) + ", " + str(b) + ")" + ": "  + str(val))
    else:
        raise ValueError("Invalid t-norm type.")
    return val

intersection = tnorm

def tconorm(a, b, tconorm_type="lukasiewicz"):
    if tconorm_type == "lukasiewicz":
        val = min(1, a + b)
        print("Lukasiewicz t-conorm("+ str(a) + ", " + str(b) + ")" + ": "  + str(val))
    elif tconorm_type == "godel":
        val = max(a, b)
        print("Godel t-conorm("+ str(a) + ", " + str(b) + ")" + ": "  + "{:.2f}".format(val))
    elif tconorm_type == "sum":
        val = (a + b) - (a * b)
        print("Probabilistic sum("+ str(a) + ", " + str(b) + ")" + ": "  + "{:.2f}".format(val))
    elif tconorm_type == "drastic":
        if a == 0:
            val = b
        elif b == 0:
            val = a
        else:
            val = 1
        print("Drastic t-conorm("+ str(a) + ", " + str(b) + ")" + ": "  + str(val))
    else:
        raise ValueError("Invalid t-conorm type.")
    return val

union = tconorm

def implication(a, b, implication_type="lukasiewicz"):
    if implication_type == "lukasiewicz":
        val = min(1, 1 - a + b)
    elif implication_type == "godel":
        if a <= b:
            val = 1
        else:
            val = b
        print("Godel implication("+ str(a) + ", " + str(b) + ")" + ": "  + "{:.2f}".format(val))
    elif implication_type == "goguen":
        if b > 0:
            val = b / a
        else:
            val = 1
        print("Goguen implication("+ str(a) + ", " + str(b) + ")" + ": "  + "{:.2f}".format(val))
    else:
        raise ValueError("Invalid implication type.")
    return val

def negation(a, negation_type="lukasiewicz"):
    if negation_type == "lukasiewicz":
        val = 1 - a
        print("Lukasiewicz negation("+ str(a) + ")" + ": " + "{:.2f}".format(val))
    elif negation_type == "godel":
        if a == 0:
            val = 1
        elif a > 0:
            val = 0
        print("Godel negation("+ str(a) + ")" + ": " + str(val))
    return val

def compute(fuzzy_set):
    core(fuzzy_set)
    support(fuzzy_set)
    cardinality(fuzzy_set)
    entropy(fuzzy_set)
    fuzziness(fuzzy_set, distance="hamming")
    fuzziness(fuzzy_set, distance="euclidean")
    gravity_center(fuzzy_set)

def compute2(a, b):
    tnorm(a, b, tnorm_type="lukasiewicz")
    tnorm(a, b, tnorm_type="godel")
    tnorm(a, b, tnorm_type="product")
    tnorm(a, b, tnorm_type="drastic")
    tconorm(a, b, tconorm_type="lukasiewicz")
    tconorm(a, b, tconorm_type="godel")
    tconorm(a, b, tconorm_type="sum")
    tconorm(a, b, tconorm_type="drastic")
    implication(a, b, implication_type="lukasiewicz")
    implication(a, b, implication_type="godel")
    implication(a, b, implication_type="goguen")
    negation(a, negation_type="lukasiewicz")
    negation(a, negation_type="godel")
    negation(b, negation_type="lukasiewicz")
    negation(b, negation_type="godel")


'''
# EXAMPLES
g = {"5": 0.3, "6": 0.5, "7": 0.9, "8": 1, "9": 0.9, "10": 0.5, "11": 0.3}
compute(g)

a = 0.7
b = 0.4
compute2(a, b)
'''
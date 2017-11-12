#read grammar
from collections import defaultdict

import math

import time

from bigfloat import bigfloat
from tree import *
N = set() #non terminal symbols
Sigma = set() #terminal symbols
R = {} #rules
S = 'TOP' #start symbol
def extract(X, i, j, back):


    result = []
    if j-i > 1:
        X, Y, Z, i, j, k = back[i][j][X]
        result.extend([back[i][j][X]])
        result.extend(extract(Y, i, k, back))
        result.extend(extract(Z, k, j, back))
    else:
        return [back[i][j][X]]
    return result
def createTree(X, i, j, back):
    if j - i > 1:
        children = []
        X, Y, Z, i, j, k = back[i][j][X]
        children.append(createTree(Y, i, k, back))
        children.append(createTree(Z, k, j, back))
        result = Node(X, children)
    else:
        _, word, _, _ = back[i][j][X]
        child = Node(word, [])
        result = Node(X, [child])
    return result
def isTermialSymbol(str):
    for s in str:
        if not s.isupper():
            return True
    return False

def isGenTwoNonTerminal(YZ):
    #print YZ
    if len(YZ.split(" ")) >=2:
        return True
    else:
        return False


#best = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda :bigfloat(0))))
#back = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))


def viterbiCKY(w):
    n = len(w)
    best = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda :bigfloat(0))))
    back = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
    for i in range(1,n+1):
        for X in N:
            if w[i-1] in R[X].keys():
                p = bigfloat(R[X][w[i-1].strip()])
                if p > best[i-1][i][X]:
                    best[i-1][i][X] = p
                    back[i-1][i][X] = (X, w[i-1], i-1, i)
    for l in range(2, n+1):
        for i in range(0, n-l+1):
            j = i + l
            for k in range(i+1, j):
                for X in N:

                    for right in R[X].keys():
                        if isGenTwoNonTerminal(right):
                            YZ = right.strip().split(" ")
                            Y = YZ[0].strip()
                            Z = YZ[1].strip()
                            p = bigfloat(R[X][right])
                            p_ = p * best[i][k][Y] * best[k][j][Z]
                            if p_ > best[i][j][X]:
                                best[i][j][X] = p_
                                back[i][j][X] = (X, Y, Z, i, j, k)
    #G_ = extract(S, 0, n, back)
    G_ = str(Tree(createTree(S, 0, n, back)))
    print(w)
    print("Prob = " + str(math.log(best[i][j][S], 10)))
    return G_



with open("grammar.txt") as f:
    count = 0
    for line in f:
        count +=1
        rule_prob = line.strip().split("#")
        prob = float(rule_prob[1].strip())
        rule = rule_prob[0].strip()
        lr = rule.split("->")
        left = lr[0].strip()
        right = lr[1].strip()
        N.add(left)


        if len(right.split(" ")) == 1:
            Sigma.add(right.strip())
        else:
            elements = right.split(" ")
            for e in elements:
                N.add(e.strip())
        if R.has_key(left):
            map = R[left]
            map[right] = prob
        else:
            R[left] = {right:prob}


runTimes = {}
runs= {}
with open("test.strings") as f:

    for line in f:
        t1 = time.clock()
        words = line.strip().split(" ")
        try:

            for i in range(len(words)):
                if words[i] not in Sigma:
                    words[i] = '<unk>'

            print(viterbiCKY(words))
        except:
            #pass
            print("")
        runningTime  = time.clock() - t1
        l = len(words)
        if(runTimes.has_key(l)):
            runTimes[l].append(runningTime)
        else:
            runTimes[l] = [runningTime]
    for l in runTimes:
        runs[l] = sum(runTimes[l]) * 1.0 / len(runTimes[l])
    for l in runTimes:
        pass
        #print(str(math.log(l)) +","+str(math.log(runs[l])))



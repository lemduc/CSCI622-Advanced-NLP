import tree
import sys, fileinput

rules = {}

def update_rules(rootNode):
    left = rootNode.label
    right = ""
    for child in rootNode.children:
        right += child.label + " "
    right = right[0:(len(right)-1)]
    if(right !=""):
        if rules.has_key(left):
            map = rules.get(left)
            if map.has_key(right):
                map[right] +=1
            else:
                map[right] = 1
        else:
            rules[left]={right: 1}
        for child in rootNode.children:
            if child is not None and child.children is not None:
                update_rules(child)
count = 1
for line in fileinput.input():

    t = tree.Tree.from_str(line)
    #print(t)
    #print t.root.label

    update_rules(t.root)

#update prob
max_count = 0
most_frequent = ""
for left in rules.keys():
    map = rules[left]
    sum = 0
    for right in map.keys():
        sum += map[right]
        if(map[right] > max_count):
            max_count = map[right]
            most_frequent = left + " -> " + right
    for right in map.keys():
        map[right] = map[right]*1.0/sum
        print(left + " -> " + right + " # " + str(map[right]))
print("max count = "+str(max_count))
print(most_frequent)
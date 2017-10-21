

with open('tagging.key') as f:
    key = f.readlines()

with open('tagging.output') as g:
    output = g.readlines()

total = 0
correct = 0

for k, o in zip(key, output):
    for x, y in zip(k.split(" "), o.split(" ")):
        total +=1
        if x == y:
            correct += 1

print("Accuracy: ", correct/total)
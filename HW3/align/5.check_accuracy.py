with open('../epron-jpron.alignment') as f:
    key = f.readlines()

with open('../epron-jpron.data') as g:
    output = g.readlines()

total = 0
correct = 0

for k, o in zip(key[2::3], output[2::3]):
    total +=1
    if k == o:
        correct += 1

print("Accuracy: ", correct/total)
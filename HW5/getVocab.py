import statistics

count = 0
line = 0
leng_line = list()
vob = set()


with open('train.en', 'r',   encoding='utf-8') as f:
    read_data = f.readlines()
for lines in read_data:
    line +=1
    leng_line.append(len(lines))
    for c in lines.split(" "):
        count +=1
        if c:
            vob.add(c)

print(count)
print(len(vob))
print(line)
print(statistics.mean(leng_line))



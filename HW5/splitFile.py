import statistics
import math
output = ""
count = 0

with open('train.en', 'r',   encoding='utf-8') as f:
    read_data = f.readlines()
    total_len  = len(read_data)
power = 5
for line in read_data:
    count +=1
    output += line
    if (count == int(total_len/(math.pow(2, power)))):
        with open(str(int((math.pow(2, power))))+'_train.en', 'w', encoding='utf-8') as f:
            f.write(output)
        power -= 1
    if power == 0:
        break


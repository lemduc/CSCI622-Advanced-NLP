import collections

start_state = final_state = 0
lastest_state = 1
mapping_state = dict()
mapping_next = dict()
output = ""

with open('epron-jpron.data') as f:
    content = f.readlines()


pairs = [content[x:x+3] for x in range(0, len(content), 3)]

for pair in pairs:
    epron_list = pair[0][:-1].split(' ')
    jpron_list = list()

    temp = pair[1][:-1].split(' ')
    for i in pair[2].split(' '):
        index = int(i)
        #print(index)
        if len(jpron_list) < index:
            jpron_list.append(temp[index-1])
        else:
            c = jpron_list[index-1]
            c = c + " " + temp[index-1]
            jpron_list[index-1] = c

    current_state = int()
    next_state = int()
    for i, e, j in zip(range(len(epron_list)), epron_list, jpron_list):
        if i == 0:
            current_state = start_state
        if (current_state, e) not in mapping_next:
            if i == len(epron_list)-1:
                next_state = final_state
            else:
                next_state = lastest_state
                lastest_state +=1
            mapping_next[(current_state, e)] = next_state
        else:
            next_state = mapping_next[(current_state, e)]

        if (current_state, e) not in mapping_state.keys():
            all_output = list()
        else:
            all_output = mapping_state[(current_state, e)]

        all_output.append(j)
        mapping_state[(current_state, e)] = all_output
        current_state = next_state

        #print (current_state, e, j)

    #break
    #print(pair)

# write wfst file
f = open('epron-jpron.wfst', 'w')
f.write('%%%%%% Filename: epron-jpron.wfst %%%%%%\n')
f.write(str(final_state) + '\n')

output = list()



for key in mapping_state.keys():
    targets = mapping_state[key]
    next    = mapping_next[key]
    count   = collections.Counter(targets)
    for k in count.keys():
        p = count[k]/len(targets)
        if (p < 0.01):
            break
        start = key[0]
        e     = key[1]
        # note: break two japanese phenomes
        split_k = k.split(" ")
        if len(split_k) > 1:
            print(start, next, e, k, p)
            temp_next = lastest_state
            lastest_state +=1
            print(start, temp_next, e, split_k[0], p)
            output.append((start, temp_next, e, split_k[0], p))
            previous = split_k[0]
            for temp in split_k[1:-1]:
                print(temp_next, lastest_state, "*e*", temp, 1.0)
                output.append((temp_next, lastest_state, "*e*", temp, 1.0))
                #previous = temp
                temp_next = lastest_state
                lastest_state +=1
            print(temp_next, next, "*e*", split_k[-1], 1.0)
            output.append((temp_next, next, "*e*", split_k[-1], 1.0))
        else:
            print(start, next, e, k, p)
            output.append((start, next, e, k, p))
    print("done")



output.sort(key=lambda tup: tup[0])
for o in output:
    f.write('({} ({} {} {} {}))'.format(*o) + "\n")
    print('({} ({} {} {} {}))'.format(*o))
f.close()

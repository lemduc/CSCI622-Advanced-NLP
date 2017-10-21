import collections

start_state = final_state = 0
lastest_state = 1
mapping_state = dict()
output = ""

with open('../epron-jpron.alignment') as f:
    content = f.readlines()


pairs = [content[x:x+3] for x in range(0, len(content), 3)]

for pair in pairs:
    epron_list = pair[0][:-1].split(' ')
    jpron_list = list()

    temp = pair[1][:-1].split(' ')
    for n, i in enumerate(pair[2].split(' ')):
        index = int(i)
        #print(index)
        if len(jpron_list) < index:
            jpron_list.append(temp[index-1])
        else:
            c = jpron_list[index-1]
            c = c + " " + temp[n]
            jpron_list[index-1] = c

    for i, e, j in zip(range(len(epron_list)), epron_list, jpron_list):

        if e not in mapping_state.keys():
            all_output = list()
        else:
            all_output = mapping_state[e]

        all_output.append(j)
        mapping_state[e] = all_output

# write wfst file
f = open('../epron-jpron-unsupervised.wfst', 'w')
f.write('%%%%%% Filename: epron-jpron.wfst %%%%%%\n')
f.write(str(final_state) + '\n')

output = list()



for key in mapping_state.keys():
    targets = mapping_state[key]
    count   = collections.Counter(targets)
    if key == "\"EY\"":
        print("\"EY\"")
    for k in count.keys():
        p = count[k]/len(targets)
        if (p < 0.01):
            continue
        e     = key
        # note: break two japanese phenomes
        split_k = k.split(" ")
        if len(split_k) > 1:
            print(0, 0, e, k, p)
            temp_next = lastest_state
            lastest_state +=1
            print(0, temp_next, e, split_k[0], p)
            output.append((0, temp_next, e, split_k[0], p))
            previous = split_k[0]
            for temp in split_k[1:-1]:
                print(temp_next, lastest_state, "*e*", temp, 1.0)
                output.append((temp_next, lastest_state, "*e*", temp, 1.0))
                #previous = temp
                temp_next = lastest_state
                lastest_state +=1
            print(temp_next, 0, "*e*", split_k[-1], 1.0)
            output.append((temp_next, 0, "*e*", split_k[-1], 1.0))
        else:
            print(0, 0, e, k, p)
            output.append((0, 0, e, k, p))
    print("done")



output.sort(key=lambda tup: tup[0])
for o in output:
    f.write('({} ({} {} {} {}))'.format(*o) + "\n")
    print('({} ({} {} {} {}))'.format(*o))
f.close()

import collections

start_state = final_state = 0
lastest_state = 1
mapping_state = dict()
mapping_next  = dict()
mapping_next['.'] = 0
mapping_next[','] = 0
total_per_state = dict()

with open('train-data') as f:
    content = f.readlines()

count = 0
current_state = 0
next_state    = 0
for line in content:
    w = line.split('/')[0].lower()
    t = line.split('/')[1][:-1]
    if w == "#" or w == "''" or w == "'" or w == ":" or w == ";" or w == "$" or w == ")" or w == "(" or w == "?" or w == "!" or w == "}" or w == "{" or w == "``" or \
            t == "#" or t == "''" or t == "'" or t == ":" or t == ";" or t == "$" or t == ")" or t == "(" or t == "?" or t == "!" or t == "}" or t == "{" or t == "``":
        # w == "." or w == "," or
        # t == "." or t == "," or
        continue
    all_tags = list()
    split_t = t.split("|")
    for single_t in split_t:
        if single_t in mapping_next:
            next_state = mapping_next[single_t]
        else:
            next_state = lastest_state
            mapping_next[single_t] = next_state
            lastest_state +=1

        if (current_state, single_t) in mapping_state.keys():
            all_tags = mapping_state[(current_state, single_t)]
        all_tags.append(w)
        mapping_state[(current_state, single_t)] = all_tags
        current_state = next_state
        count += 1
        #print(single_t,w)

print(count)
# write wfst file
f = open('bigram.wfsa', 'w')
f.write('%%%%%% Filename: bigram.wfsa %%%%%%\n')
f.write(str(final_state) + '\n')


output = list()

for key in mapping_state.keys():
    state = key[0]
    total = 0
    if state in total_per_state.keys():
        total = total_per_state[state]
    total += len(mapping_state[key])
    total_per_state[state] = total

for key in mapping_state.keys():
    state = key[0]
    tag = key[1]
    next_state = mapping_next[tag]
    p = len(mapping_state[key])/total_per_state[state]
    output.append((state, next_state, tag, p))
    #print("done")

output.sort(key=lambda tup: tup[0])
for o in output:
    f.write('({} ({} "{}" {}))'.format(*o) + "\n")
    print('({} ({} "{}" {}))'.format(*o))
f.close()
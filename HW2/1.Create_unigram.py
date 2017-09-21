import collections

start_state = final_state = 0
lastest_state = 1
mapping_state = dict()

with open('train-data') as f:
    content = f.readlines()

count = 0
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
        if single_t in mapping_state.keys():
            all_tags = mapping_state[single_t]
        all_tags.append(w)
        mapping_state[single_t] = all_tags
        count += 1
        #print(single_t,w)

print(count)
# write wfst file
f = open('unigram.wfsa', 'w')
f.write('%%%%%% Filename: unigram.wfsa %%%%%%\n')
f.write(str(final_state) + '\n')


output = list()

for key in mapping_state.keys():
    p = len(mapping_state[key])/count
    output.append((0, 0, key, p))
    #print("done")

output.sort(key=lambda tup: tup[0])
for o in output:
    f.write('({} ({} "{}" {}))'.format(*o) + "\n")
    print('({} ({} "{}" {}))'.format(*o))
f.close()
#test_string = "that is a test ."
#test_string = "the fly knows how to fly ."
test_string = "the company has agreed to release its tax returns since 1985 , and those of its affiliates and partnerships ."

# read bigram
bigram = dict()
tag_set = set()
with open('bigram.wfsa') as f:
    content = f.readlines()

for line in content[2:]:
    split = line[:-1].replace("(", "").replace(")","").replace("\"","").split(" ")
    start = split[0]
    next  = split[1]
    tag = split[2]
    p = split[3]
    tag_set.add(tag)
    bigram[(start, tag)] = (next, float(p))

# read tag-to-word
tag_to_word_p = dict()
with open('tag-to-word.wfst') as f:
    content = f.readlines()

for line in content[2:]:
    split = line[:-1].replace("(", "").replace(")","").replace("\"","").split(" ")
    tag = split[2]
    word = split[3]
    p = split[4]
    tag_to_word_p[(tag, word)] = float(p)

#implement viterbi

#initiate
total_tags = len(tag_set) # based on unigram
split_input = test_string.split(" ")
total_word_length = len(split_input)
Q = {}
Q_next_state = {}
best_pred = {}
count_non_zero = 0

#first column
w = split_input[0]
tag_list = list(tag_set)
for i in range(len(tag_list)):
    tag = tag_list[i]
    if (tag, w) not in tag_to_word_p.keys():
        Q[0, i] = 0
        Q_next_state[0, i] = "0"
        #print(tag + " 0")
    else:
        p_tag_word = tag_to_word_p[(tag, w)]
        (next, p_tag_state) = bigram[("0", tag)]
        Q_next_state[0, i] = next
        Q[0, i] = p_tag_state*p_tag_state
        count_non_zero +=1
    print(Q[0, i])

#update the rest
for i in range(1, len(split_input)-1):
    print("loop " + str(i))
    w = split_input[i]
    for j in range(len(tag_list)):
        tag = tag_list[j]
        Q[i,j] = 0
        best_pred[i,j] = 0
        best_score = float("-inf")
        for k in range(len(tag_list)):
            prev_tag = tag_list[k]
            pre_state = Q_next_state[i-1,k]
            if (pre_state, tag) not in bigram.keys():
                next = "0"
                p_tag_state = 0
            else:
                next, p_tag_state = bigram[(pre_state, tag)]
            if (tag, w) not in tag_to_word_p.keys():
                p_tag_word = 0
            else:
                p_tag_word        = tag_to_word_p[tag, w]
            r = Q[i-1,k]*p_tag_word*p_tag_state
            if r > best_score:
                best_score = r
                best_pred[i, j] = k
                Q[i,j] = r
                Q_next_state[i, j] = next
        print(Q[i, j])
        if Q[i, j] > 0:
            count_non_zero +=1

final_best = 0
final_score = float("-inf")
for j in range(len(tag_list)-2):
    if Q[len(split_input)-2, j] > final_score:
        final_score = Q[len(split_input)-2, j]
        final_best  = j

print("final best:" + tag_list[j])
current = final_best
for i in reversed(range(len(split_input)-2)):
    current = best_pred[i+1, current]
    print("previous best:" + tag_list[current])

print('None zero cells: ' + str(count_non_zero))
print('Percentage of none zero cells: ' + str(count_non_zero*100/((total_word_length-1)*total_tags)))
print('done')
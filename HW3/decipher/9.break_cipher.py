#compute the letter-bigram model
from string import ascii_uppercase
import math
from collections import defaultdict

with open('../english.data') as f:
    lines = f.readlines()

bigram_count = dict()
#unigram_count = defaultdict(lambda: 0)
bigram_prob = dict()
bigram_prob_log = defaultdict(lambda:  float("-inf"))

for l in lines:
    line = l[:-1] # remove \n
    for num, char in enumerate(list(line)):
        pair = tuple()
        if num == 0:
            pair = (" ", char)
        else:
            pair = (list(line)[num-1],char)

        if pair not in bigram_count.keys():
            bigram_count[pair] = 1
        else:
            bigram_count[pair] += 1
        #unigram_count[char] += 1
    last_pair = (list(line)[-1], " ")
    if last_pair not in bigram_count.keys():
        bigram_count[last_pair] = 1
    else:
        bigram_count[last_pair] += 1


print('done counting')

for c in ascii_uppercase + (" "):
    #print(c)
    total = 0
    for d in ascii_uppercase + (" "):
        if (c,d) in bigram_count.keys():
            total += bigram_count[(c,d)]
    #print(total)
    for d in ascii_uppercase + (" "):
        if (c,d) in bigram_count.keys():
            bigram_prob[(c,d)] = bigram_count[(c,d)]/total
        else:
            bigram_prob[(c, d)] = 0

for key in bigram_prob:
    #print(bigram_prob[key])
    if (bigram_prob[key] != 0):
        bigram_prob_log[key] = math.log(bigram_prob[key])

print('done probability')

# implement EM forward backword

def viterbi(sequence, tag_set, bigram_dict, word_tag_dict):
    Q = defaultdict(lambda: defaultdict(lambda: float("-inf")))
    best_pred = defaultdict(lambda: defaultdict(lambda: 0))
    for tag in tag_set:
        Q[0][tag] = bigram_dict[(" ", tag)] + word_tag_dict[tag][sequence[0]]

    for i in range(1, len(sequence)):
        for tag_2 in tag_set:
            Q[i][tag_2] = float("-inf")
            best_pred[i][tag_2] = None
            best_score = float("-inf")

            for tag_1 in tag_set:
                r = bigram_dict[(tag_1, tag_2)] + word_tag_dict[tag_2][sequence[i]] + Q[i - 1][tag_1]
                if r > best_score:
                    best_score = r
                    best_pred[i][tag_2] = tag_1
                    Q[i][tag_2] = r

    final_best = None
    final_score = float("-inf")
    best_tags = []
    for tag in tag_set:
        if Q[len(sequence) - 1][tag] > final_score:
            final_score = Q[len(sequence) - 1][tag]
            final_best = tag
    best_tags.append(final_best)

    current = final_best
    for i in range(len(sequence) - 2, -1, -1):
        current = best_pred[i + 1][current]
        best_tags.append(current)
    # print(best_tags)
    return reversed(best_tags)

def add(log_x, log_y):
    if log_x == float("-inf"):
        return log_y
    if log_y == float("-inf"):
        return log_x
    if (log_x - log_y > 16):
        return log_x
    if (log_x >= log_y ):
        return log_x + math.log(1+math.exp(log_y-log_x))
    if (log_y - log_x > 16):
        return log_y
    if (log_y > log_x ):
        return log_y + math.log(1+math.exp(log_x-log_y))

def decifer(cipher: str, bigram_dict: dict, iter: int):
    decifer_map = defaultdict(lambda : defaultdict(lambda: float("-inf")))

    for it in range(iter):
        fwd = defaultdict(lambda : defaultdict(lambda: float("-inf")))
        bkw = defaultdict(lambda : defaultdict(lambda: float("-inf")))

        if it == 0:
            for d in ascii_uppercase:
                for c in ascii_uppercase:
                    decifer_map[d][c] = math.log(1/len(ascii_uppercase))
            decifer_map[" "][" "] = 0
        else:
            for i, char in enumerate(cipher):
                if i == 0:
                    for c in ascii_uppercase + " ":
                        fwd[i][c] = bigram_dict[(" ", c)] + decifer_map[c][char]
                else:
                    for c in ascii_uppercase + " ":
                        for p in ascii_uppercase + " ":
                            fwd[i][c] = add(fwd[i][c], fwd[i-1][p] + bigram_dict[(p, c)] + decifer_map[c][char] )

            fwd_prob = float("-inf")
            for e in ascii_uppercase + " ":
                fwd_prob = add(fwd_prob, fwd[len(cipher)-1][e])

            print(fwd_prob)

            for i in range(len(cipher)-1,-1,-1):
                if i == len(cipher) -1:
                    for c in ascii_uppercase + " ":
                        bkw[i][c] = 0
                else:
                    for c in ascii_uppercase + " ":
                        for n in ascii_uppercase + " ":
                            bkw[i][c] = add(bkw[i][c], bkw[i+1][n] + decifer_map[n][cipher[i+1]] + bigram_dict[(c,n)])

            bkw_prob = float("-inf")

            for c in bkw[0]:
                bkw_prob = add(bkw_prob, bkw[0][c] + bigram_dict[(" ",c)] + decifer_map[c][cipher[0]])

            assert abs(bkw_prob-fwd_prob) < 0.0001

            pair_count_dict = defaultdict(lambda: defaultdict(lambda: float("-inf")))
            count_dict = defaultdict(lambda: float("-inf"))

            for idx, c in enumerate(cipher):
                for d in ascii_uppercase + " ":
                    pair_count_dict[d][c] = add(pair_count_dict[d][c], fwd[idx][d] + bkw[idx][d] - fwd_prob)
                    count_dict[d] = add(count_dict[d], fwd[idx][d] +  bkw[idx][d] - fwd_prob)

            #decifer_map = defaultdict(lambda: defaultdict(lambda: float("-inf")))

            for d in pair_count_dict:
                for c in pair_count_dict[d]:
                    # print(eletter, cletter, pair_count_dict[eletter][cletter], count_dict[eletter])
                    assert pair_count_dict[d][c] <= count_dict[d]
                    if count_dict[d] == float("-inf"):
                        decifer_map[d][c] = float("-inf")
                    else:
                        decifer_map[d][c] = pair_count_dict[d][c] - count_dict[d]

        if it <= 5 or it == iter -1 :
            print("".join(viterbi(cipher, ascii_uppercase + " ", bigram_dict, decifer_map)))

        if it == iter - 1:
            for c in ascii_uppercase + " ":
                print("orginal: "+c)
                for d in ascii_uppercase + " ":
                    if decifer_map[c][d] > math.log(0.01):
                        print(d + " " + str(math.exp(decifer_map[c][d])))

    return decifer_map



c = []
with open("../cipher.data") as f:
    c = f.read()

dec = decifer(c[:-1], bigram_prob_log, 100)
#print(dec)
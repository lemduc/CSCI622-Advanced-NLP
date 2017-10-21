import math
import string
from collections import defaultdict


def add(log_x, log_y):
    # print("add", log_x, log_y)
    if log_x == float("-inf"):
        return log_y
    if log_y == float("-inf"):
        return log_x
    if log_x - log_y > 16:
        return log_x
    if log_y - log_x > 16:
        return log_y
    if log_x >= log_y:
        return log_x + math.log(1 + math.exp(log_y - log_x))
    if log_y > log_x:
        return log_y + math.log(1 + math.exp(log_x - log_y))


def bigram(text):
    bigram_dict = defaultdict(lambda: 0.0)
    unigram_dict = defaultdict(lambda: 0.0)
    text = text.replace("\n", " ")
    for idx, letter in enumerate(text):
        if idx > 0:
            bigram_dict[(text[idx - 1], letter)] += 1
        unigram_dict[letter] += 1

    log_bigram_dict = defaultdict(lambda: float("-inf"))

    for gram_1, gram_2 in bigram_dict:
        log_bigram_dict[(gram_1, gram_2)] = math.log(bigram_dict[(gram_1, gram_2)] / unigram_dict[gram_1])

    return log_bigram_dict


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


def em_train(ciphertext, bigram_dict, iteration):
    ciphertext = ciphertext.replace("\n", "")
    decipher_table = defaultdict(lambda: defaultdict(lambda: float("-inf")))

    for i in range(iteration):
        forward_table = defaultdict(lambda: defaultdict(lambda: float("-inf")))
        backward_table = defaultdict(lambda: defaultdict(lambda: float("-inf")))

        if i == 0:
            for letter_1 in string.ascii_uppercase:
                for letter_2 in string.ascii_uppercase:
                    decipher_table[letter_1][letter_2] = math.log(1.0 / len(string.ascii_uppercase))
            decipher_table[" "][" "] = 0
        else:
            for idx, cletter in enumerate(ciphertext):
                if idx == 0:
                    for eletter_2 in string.ascii_uppercase + " ":
                        forward_table[idx][eletter_2] = bigram_dict[(" ", eletter_2)] + decipher_table[eletter_2][
                            cletter]
                # elif cletter == " ":
                #     for eletter_1 in string.ascii_uppercase + " ":
                #         forward_table[idx][" "] = add(forward_table[idx][" "],
                #                                       forward_table[idx - 1][eletter_1] +
                #                                       bigram_dict[(eletter_1, " ")])
                #         # print(cletter, eletter_1, forward_table[idx][" "])
                else:
                    for eletter_2 in string.ascii_uppercase + " ":
                        for eletter_1 in string.ascii_uppercase + " ":
                            forward_table[idx][eletter_2] = add(forward_table[idx][eletter_2],
                                                                forward_table[idx - 1][eletter_1] +
                                                                decipher_table[eletter_2][cletter] +
                                                                bigram_dict[(eletter_1, eletter_2)])
            forward_prob = float("-inf")
            for eletter in forward_table[len(ciphertext) - 1]:
                forward_prob = add(forward_prob,
                                   forward_table[len(ciphertext) - 1][eletter])

            print(forward_prob)

            for idx in range(len(ciphertext) - 1, -1, -1):
                if idx == len(ciphertext) - 1:
                    for eletter_2 in string.ascii_uppercase + " ":
                        backward_table[idx][eletter_2] = 0
                # elif ciphertext[idx + 1] == " ":
                #     for eletter_2 in string.ascii_uppercase + " ":
                #         backward_table[idx][eletter_2] = add(backward_table[idx][eletter_2],
                #                                              backward_table[idx + 1][" "] +
                #                                              bigram_dict[(eletter_2, " ")])
                else:
                    for eletter_2 in string.ascii_uppercase + " ":
                        for eletter_1 in string.ascii_uppercase + " ":
                            backward_table[idx][eletter_2] = add(backward_table[idx][eletter_2],
                                                                 backward_table[idx + 1][eletter_1] +
                                                                 decipher_table[eletter_1][ciphertext[idx + 1]] +
                                                                 bigram_dict[(eletter_2, eletter_1)])

            backward_prob = float("-inf")
            for eletter in backward_table[0]:
                backward_prob = add(backward_prob,
                                    backward_table[0][eletter] + bigram_dict[(" ", eletter)] + decipher_table[eletter][
                                        ciphertext[0]])

            # print(backward_prob)
            assert abs(backward_prob - forward_prob) < 0.0001
            pair_count_dict = defaultdict(lambda: defaultdict(lambda: float("-inf")))

            count_dict = defaultdict(lambda: float("-inf"))
            for idx, cletter in enumerate(ciphertext):
                for eletter in string.ascii_uppercase + " ":
                    pair_count_dict[eletter][cletter] = add(pair_count_dict[eletter][cletter],
                                                            forward_table[idx][eletter] +
                                                            backward_table[idx][eletter] - forward_prob)
                    count_dict[eletter] = add(count_dict[eletter],
                                              forward_table[idx][eletter] +
                                              backward_table[idx][eletter] - forward_prob)

            # pprint(count_dict)
            # pprint(pair_count_dict)

            decipher_table = defaultdict(lambda: defaultdict(lambda: float("-inf")))

            for eletter in pair_count_dict:
                for cletter in pair_count_dict[eletter]:
                    # print(eletter, cletter, pair_count_dict[eletter][cletter], count_dict[eletter])
                    assert pair_count_dict[eletter][cletter] <= count_dict[eletter]
                    if count_dict[eletter] == float("-inf"):
                        decipher_table[eletter][cletter] = float("-inf")
                    else:
                        decipher_table[eletter][cletter] = pair_count_dict[eletter][cletter] - count_dict[eletter]

        if i <= 5:
            print("".join(viterbi(ciphertext, string.ascii_uppercase + " ", bigram_dict, decipher_table)))
    return decipher_table


if __name__ == "__main__":
    with open("english.data", "r") as reader:
        text = reader.read()
    bigram_dict = bigram(text)

    with open("cipher.data", "r") as reader:
        text = reader.read()
    decipher = (em_train(text, bigram_dict, 200))
    # pprint(decipher)

with open('../epron-jpron-unsupervised.data') as f:
    content = f.readlines()


pairs = [content[x:x+2] for x in range(0, len(content), 3)]

def recursiveGen(eng, jpn):
    returnList = list()
    if len(eng) == 1:
        pair = (eng[0], jpn)
        tmp = list()
        tmp.append(pair)
        returnList.append(tmp)
    else:
        gap = len(jpn) - len(eng)
        e_pro = eng[0]
        for i in range(gap+1):
            j_pro = jpn[:i+1]
            pair = (e_pro, j_pro)
            restOfTheList = recursiveGen(eng[1:], jpn[i+1:])
            for item in restOfTheList:
                returnList.append((pair, *item))

    return returnList

def EM_Algo(all_alg):

    #1.
    it = 0
    out_alignment = ""
    total_it = 10
    p_dict = dict()
    count_dict = dict()
    alg_set  = set()
    while (it < total_it):
        count_sen = -1
        print("Iter " + str(it))
        for pair_set in all_alg:
            count_sen += 1
            total_alg = len(pair_set)
            #2a.
            for sentence in pair_set:
                for item in sentence:
                    alg_set.add((item[0], *item[1]))

            # 2b.
            if it == 0:
                for num, alg  in enumerate(pair_set):
                    p_dict[str(alg)] = 1/total_alg
            else:
                for num, alg  in enumerate(pair_set):
                    p_dict[str(alg)] = 1
                    for pair in alg:
                        p_dict[str(alg)] *= p_dict[(pair[0], *pair[1])]
                total = 0
                for num, alg  in enumerate(pair_set):
                    total += p_dict[str(alg)]
                max_p = 0
                max_alg = list()
                for num, alg  in enumerate(pair_set):
                    p_dict[str(alg)] /= total
                    if p_dict[str(alg)]>max_p:
                        max_p =  p_dict[str(alg)]
                        max_alg = alg
                if (count_sen < 5):
                    print(str(max_alg) + " " + str(max_p))
                if (it == 9):
                    print(max_alg)
                    eng_str = ""
                    jpn_str = ""
                    alg_str = ""
                    count = 0
                    for item in max_alg:
                        count += 1
                        eng_str += item[0] + " "
                        for c in range(len(item[1])):
                            jpn_str += str(item[1][c]) + " "
                            alg_str += str(count) + " "
                    out_alignment += eng_str[:-1] + '\n' +jpn_str[:-1] + '\n' + alg_str[:-1] + '\n'

            # 2c.
            for num, alg in enumerate(pair_set):
                for k in range(len(alg)):
                    key = (alg[k][0], *alg[k][1])
                    if key not in count_dict.keys():
                        count_dict[key] = 0
                    count_dict[key] += p_dict[str(alg)]

        #print('done step 2')
        #3 normalize
        total = 0
        for k in count_dict.keys():
            total += count_dict[k]
        for k in count_dict.keys():
            p_dict[k] = count_dict[k] /total
        #4.
        for k in count_dict.keys():
            count_dict[k] = 0

        it += 1

    return out_alignment
    #print('done EM')

whole_alg = list()

for pair in pairs:
    #print(pair[0])
    #print(pair[1])
    eng = pair[0][:-1].split(" ")
    jpn = pair[1][:-1].split(" ")
    returnList = recursiveGen(eng, jpn)
    for sentence in returnList:
        eng_str = ""
        jpn_str = ""
        alg_str = ""
        count = 0
        for item in sentence:
            count +=1
            eng_str += item[0] + " "
            for c in range(len(item[1])):
                jpn_str += str(item[1][c]) + " "
                alg_str += str(count) + " "
        #print(eng_str[:-1] )
        #print(jpn_str[:-1] )
        #print(alg_str[:-1] )
    whole_alg.append(returnList)

out = EM_Algo(whole_alg)

with open("../epron-jpron.alignment", "w") as myfile:
    myfile.write(out)


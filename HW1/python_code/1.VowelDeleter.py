import string

output = ""

f = open('vowel-deleter.fst', 'w')
f.write('%%%%%% Filename: vowel-deleter.fst %%%%%%\n')
f.write('0\n')

for c in string.ascii_uppercase:
    if c in ["A", "E", "I","O","U"]:
        out = '(0 (0 "{}" {}))'.format(c, '*e*')
    else:
        out = '(0 (0 "{}" "{}"))'.format(c, c)
    print(out)
    f.write(out + '\n')
f.write('(0 (0 "{}" "{}"))'.format('_', '_') + '\n')
f.close()
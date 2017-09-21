import string

output = ""

f = open('space-deleter.fst', 'w')
f.write('%%%%%% Filename: space-deleter.fst %%%%%%\n')
f.write('0\n')

for c in string.ascii_uppercase:
    out = '(0 (0 "{}" "{}"))'.format(c, c)
    f.write(out + '\n')
f.write('(0 (0 "{}" {}))'.format('_', '*e*') + '\n')
f.close()
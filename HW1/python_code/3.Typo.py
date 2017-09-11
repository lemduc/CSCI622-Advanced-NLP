import string
KeyboardRow1 = ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", ""]
KeyboardRow2 = ["", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", ""]
KeyboardRow3 = ["", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "", "", ""]
KeyboardRow4 = ["", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "", "", ""]
KeyboardRow1S = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", ""]
KeyboardRow2S = ["", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"]
KeyboardRow3S = ["","A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "", "", ""]
KeyboardRow4S = ["", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "", "", ""]
Array2R = [KeyboardRow1, KeyboardRow2, KeyboardRow3, KeyboardRow4]
Array2S = [KeyboardRow1S, KeyboardRow2S, KeyboardRow3S, KeyboardRow4S]
Array3 = [Array2R, Array2S]


def getindex(character):
    for row, x in zip(Array2S, range(0,4)):
        if character in row:
            #print('{}, {}'.format(x, row.index(character)))
            return x, row.index(character)
    return -1, -1

output = ""

f = open('typo.fst', 'w')
f.write('%%%%%% Filename: typo.fst %%%%%%\n')
# end state
f.write('3\n')

#first correct character
for c in string.ascii_uppercase:
    out = '(0 (1 "{}" "{}"))'.format(c, c)
    f.write(out + '\n')
# handle if the string ends
f.write('(0 (3 {} {}))'.format('*e*', '*e*') + '\n')
f.write('(0 (0 "{}" "{}"))'.format('_', '_') + '\n')

#second correct character
for c in string.ascii_uppercase:
    out = '(1 (2 "{}" "{}"))'.format(c, c)
    f.write(out + '\n')
#handle if the string ends
f.write('(1 (3 {} {}))'.format('*e*', '*e*') + '\n')
f.write('(1 (1 "{}" "{}"))'.format('_', '_') + '\n')

#third wrong character
for c in string.ascii_uppercase:
    x, y = getindex(c)
    print('{}, {}, {}'.format(c, x, y))
    for i in range(-1,2):
        for j in range(-1, 2):
            if x+i in range(0,4) and y+j in range(0, 12):
                typo = Array2S[x+i][y+j]
                if typo in string.ascii_uppercase and typo != c and typo != '':
                    print('{}, {}, {}'.format(x + i, y + j, typo))
                    f.write('(2 (0 "{}" "{}"))'.format(c, typo) + '\n')

#handle if the string ends
f.write('(2 (3 {} {}))'.format('*e*', '*e*') + '\n')
f.write('(2 (2 "{}" "{}"))'.format('_', '_') + '\n')

f.close()
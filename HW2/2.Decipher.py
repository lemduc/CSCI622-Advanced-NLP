plain = "a quick brown fox jumps over the lazy dog"
cipher = "s wiovl ntpem gpc kizqd pbrt yjr asxu fph"


f = open('decipher.wfst', 'w')
f.write('%%%%%% Filename: decipher.wfst %%%%%%\n')
f.write(str(0) + '\n')


print_space = False
for c, p in zip(list(cipher), list(plain)):
    if c == " ":
        if not print_space:
            print_space = True
        else:
            continue
    print('({} ({} "{}" "{}"))'.format(str(0), str(0), c, p))
    f.write('({} ({} "{}" "{}"))'.format(str(0), str(0), c, p) + '\n')

f.close()
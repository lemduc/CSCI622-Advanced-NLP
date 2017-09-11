start_state = 0
final_state = None
state_count = 1
state_mapping = dict()
output = ""
has_appeared = set()

#with open('spanishvocab_short.txt') as f:
with open('spanishvocab.txt') as f:
    content = f.readlines()

for line in content:
    current_state = 0
    if not line.endswith(' \n'):
        line = line[:-1] + " \n"
    # print(line)
    for c in line.split(' '):
        next_state = int()
        if c == "\n":
            c = '*e*'
        if (current_state, c) not in state_mapping.keys():
            if c != '*e*':
                state_mapping[(current_state, c)] = state_count
                next_state = state_count
                state_count += 1
            else:
                if final_state is not None:
                    next_state = final_state
                else:
                    next_state = state_count
                    final_state = state_count
                    state_count += 1
        else:
            next_state = state_mapping[(current_state, c)]
        if c != '*e*':
            s = '({} ({} \"{}\"))'.format(current_state, next_state, c)
            print(s)
            if s not in has_appeared:
                output += s + "\n"
                has_appeared.add(s)
        else:
            # go to final state
            s = '({} ({} {}))'.format(current_state, next_state, c)
            # go back to start state
            s_s = '({} ({} {}))'.format(current_state, start_state, c)
            print(s)
            if s not in has_appeared:
                output += s + "\n"
                has_appeared.add(s)
            if s_s not in has_appeared:
                output += s_s + "\n"
                has_appeared.add(s_s)
        current_state = next_state

        # print(state_count)

# write fsa file
f = open('spanish.fsa', 'w')
f.write('%%%%%% Filename: spanish.fsa %%%%%%\n')
f.write(str(final_state) + '\n')
f.write(output)
# able to accept space (aka "_" in this case)
f.write('({} ({} \"{}\"))'.format(start_state, start_state, "_"))
f.close()

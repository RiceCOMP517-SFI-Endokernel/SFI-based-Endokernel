cc = '/home/jerry/sfi-llvm/llvm/build/bin/clang'


if __name__ == '__main__':
    # all = ''
    new_lines = []
    with open('makefile.txt', 'r') as file:
        s = file.read()
        s = s.replace('\\'+'\n', '')
        # print(s)
        lines = s.split('\n')

        for line in lines:
            if line.endswith(".c"):
                print(line)
                line = line.replace(".c", ".optbc")
                print(line)
            if len(line.strip()) == 0:
                # continue
                pass
            new_lines.append(line)

    with open('makefile.new', 'w') as file:
        file.write("\n".join(new_lines))



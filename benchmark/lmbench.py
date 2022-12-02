from pickle import FALSE
import subprocess
import os
import variable
import time

start_time = time.time()

# Prepare test file
os.system("dd if=/dev/urandom of=/tmp/test.bin bs=1024 count=1024")

tests = dict()
tests.update({'null':'lat_syscall null'})
tests.update({'open':'lat_syscall open'})
tests.update({'read':'lat_syscall read'})
tests.update({'write':'lat_syscall write'})
tests.update({'mmap':'lat_mmap 512k /tmp/test.bin'})
# tests.update({'bw_copy': 'bw'})
tests.update({'bw_copy' : 'bw_mem 1m cp'})
tests.update({'bw_rd' : 'bw_mem 1m rd'})
tests.update({'bw_wr' : 'bw_mem 1m wr'})
tests.update({'bw_rdwr' : 'bw_mem 1m rdwr'})


variable.set_name("lmbench")
variable.def_test("lmbench", variable.get_row(), tests.keys())
variable.tries = 1
n = 0
for i in range(0, len(variable.iv_nocet_paths)):
    if variable.iv_nocet_paths[i] == "baseline":
        filesuffix = "lmbench_baseline"
        cmdprefix = '../lmbench-2.5/bin/x86_64-linux-gnu/'
        tname = 'baseline '
    else:
        filesuffix = "lmbench_" + variable.iv_nocet_paths[i].split("/")[-2]
        cmdprefix = variable.iv_nocet_paths[i] + "libintravirt.so " + variable.glibcpath + " ../lmbench-2.5/bin/x86_64-linux-gnu/"
        tname = variable.iv_nocet_paths[i].split("/")[-2]

    resfilename = "" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    fp.write(b'null,open,read,write,mmap,bw_mem copy,bw_mem rd,bw_mem wr,bw_mem rdwr\n')

    for j in range(0, variable.tries):
        for curtest in tests.keys():
            okay = False
            while not okay:
                cmd = cmdprefix + tests[curtest]
                print(f"cmd = {cmd}")
                print('line 45:' + tname + " " + curtest + ": " + str(j))
                ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                try:
                    if curtest.startswith('mmap'):
                        err = ps.stderr.read()
                        output = err.split(b' ')[1][:-1]
                    elif curtest.startswith('bw_'):
                        err = ps.stderr.read()
                        output = err.split(b' ')[1][:-1]
                    else:
                        output = ps.stderr.read().splitlines()[0].split(b'[')[1][5:11]
                    print(f"output = {output}")
                    variable.add_result('lmbench', n, curtest, float(output))
                    fp.write(output)
                    fp.write(b',')
                    print("OK!")
                    okay = True
                except Exception as e:
                    print(e)
                    exit(0)
                    okay = False
        fp.write(b'\n')
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)
    n = n + 1


### now SFI's turn
for i in range(0, len(variable.iv_cet_paths)):
    if variable.iv_cet_paths[i] == "baseline":
        filesuffix = "SFI_lmbench_baseline"
        cmdprefix = '../lmbench-2.5-sfi/bin/x86_64-linux-gnu/'
        tname = 'baseline '
    else:
        filesuffix = "SFI_lmbench_" + variable.iv_cet_paths[i].split("/")[-2]
        cmdprefix = variable.iv_cet_paths[i] + "libintravirt.so " + variable.cet_glibcpath + " ../lmbench-2.5-sfi/bin/x86_64-linux-gnu/"
        tname = variable.iv_cet_paths[i].split("/")[-2]

    resfilename = "./" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    fp.write(b'null,open,read,write,mmap,bw_mem copy,bw_mem rd,bw_mem wr,bw_mem rdwr\n')

    for j in range(0, variable.tries):
        for curtest in tests.keys():
            cmd = cmdprefix + tests[curtest]
            print(tname + " " + curtest + ": " + str(j))
            ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

            if curtest.startswith('mmap'):
                output = ps.stderr.read().split(b' ')[1][:-1]
            elif curtest.startswith('bw_'):
                err = ps.stderr.read()
                output = err.split(b' ')[1][:-1]
            else:
                output = ps.stderr.read().splitlines()[0].split(b'[')[1][5:11]
            fp.write(output)
            fp.write(b',')
            variable.add_result('lmbench', n, curtest, float(output))
            print(output)
        fp.write(b'\n')
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)
    n = n + 1


total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("Lmbench total time: " + printable_time)
os.system("echo \"Lmbench: " + printable_time +"\" >> ./" + variable.resdir + "/time.txt")

variable.save()



# 100000 - 1FFFFF  |ENDOKERNEL| 
# 200000 - 2FFFFF |USER PROGRAM|

# 200000

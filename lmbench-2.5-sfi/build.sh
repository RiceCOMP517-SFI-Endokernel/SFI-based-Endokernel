/home/jerry/sfi-llvm/llvm/build/bin/clang -c -emit-llvm src/lat_syscall.c

/home/jerry/sfi-llvm/llvm/build/bin/opt -enable-new-pm=0 -load ../sfi-llvm/llvm/build/lib/LLVMSFI.so -sfi --enable-sfi-loadchecks --enable-sfi-svachecks -o lat_syscall_inst.bc lat_syscall.bc

/home/jerry/sfi-llvm/llvm/build/bin/opt -O3 -o lat_syscall_opt.bc lat_syscall_inst.bc 

/home/jerry/sfi-llvm/llvm/build/bin/clang -o lat_syscall lat_syscall_opt.bc bin/x86_64-linux-gnu/lmbench.a -lm




/home/jerry/sfi-llvm/llvm/build/bin/clang -c -emit-llvm src/lat_mmap.c
/home/jerry/sfi-llvm/llvm/build/bin/opt -enable-new-pm=0 -load ../sfi-llvm/llvm/build/lib/LLVMSFI.so -sfi --enable-sfi-loadchecks --enable-sfi-svachecks -o lat_mmap_inst.bc lat_mmap.bc
/home/jerry/sfi-llvm/llvm/build/bin/opt -O3 -o lat_mmap_opt.bc lat_mmap_inst.bc 
/home/jerry/sfi-llvm/llvm/build/bin/clang -o lat_mmap lat_mmap_opt.bc bin/x86_64-linux-gnu/lmbench.a -lm

EXE=bw_mem
/home/jerry/sfi-llvm/llvm/build/bin/clang -c -emit-llvm src/$EXE.c
/home/jerry/sfi-llvm/llvm/build/bin/opt -enable-new-pm=0 -load ../sfi-llvm/llvm/build/lib/LLVMSFI.so -sfi --enable-sfi-loadchecks --enable-sfi-svachecks -o "$EXE"_inst.bc $EXE.bc
/home/jerry/sfi-llvm/llvm/build/bin/opt -O3 -o "$EXE"_opt.bc "$EXE"_inst.bc 
/home/jerry/sfi-llvm/llvm/build/bin/clang -o "$EXE" "$EXE"_opt.bc bin/x86_64-linux-gnu/lmbench.a -lm

/home/jerry/sfi-llvm/llvm/build/bin/clang -c -pipe  -O -W -Wall -Wpointer-arith \
-Wno-unused-parameter -Werror -g -fno-stack-protector -fno-jump-tables -isystem src/core        -isystem src/event \
-isystem src/event/modules -isystem src/os/unix -isystem objs -o objs/src/core/nginx.o src/core/nginx.optbc
#!/bin/bash
src/parser.py test/$1 2> t > temp.ir
src/codegen.py temp.ir > temp.s
gcc -m32 -g temp.s -o temp
./temp
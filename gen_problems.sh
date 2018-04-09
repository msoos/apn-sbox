#!/usr/bin/bash

# 36 is kind of interesting
./sbox.py --num 6
cat problem6_simp.xnf > tmp
./cnf-utils/xor_to_cnf.py tmp "tmp_converted"
for i in  {0..40}; do
    echo "Doing ${i}"
    cat tmp_converted > tmp
    ./sbox.py -n 6 --hb ${i} --onlyhelp >> tmp
    ./cnf-utils/xor_to_cnf.py tmp "sbox_problem_${i}.cnf"
done

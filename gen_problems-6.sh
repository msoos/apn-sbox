#!/usr/bin/bash

# 36 is kind of interesting
./sbox.py --num 6
cat problem6_simp.xnf > tmp
./cnf-utils/xor_to_cnf.py --cutsize 3 tmp tmp_converted_3
./cnf-utils/xor_to_cnf.py --cutsize 4 tmp tmp_converted_4
./cnf-utils/xor_to_cnf.py --cutsize 5 tmp tmp_converted_5
for i in  {20..40}; do
    for i2 in  {3..5}; do
        echo "Doing ${i} -- cut $i2"
        cat tmp_converted_$i2 > tmp
        ./sbox.py -n 6 --hb ${i} --onlyhelp >> tmp
        ./cnf-utils/xor_to_cnf.py tmp "apn-sbox6-cut${i2}-helpbox${i}.cnf"
    done
done

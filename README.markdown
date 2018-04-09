# sbox
Almost perfect non-linear (APN) S-box finder. These s-boxes provide optimal resistance against differential attacks. Dillon et al. has constructed one s-box in n=6 in 2009. If you can solve this, you can construct one too. Set s=8 and try to solve :)

Many thanks to Ivica Nikolic for the problem description and then many discussions.

To generate problems in n=6 to re-create Dillon's result:

```
git clone https://github.com/msoos/sbox
cd sbox
git submodule init
git submodule update
./gen_problems.sh
lingeling sbox_problem_36.cnf
(will solve in some seconds)
```

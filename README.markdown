# APN S-box generator
Almost perfect non-linear (APN) S-box finder. These S-boxes provide optimal resistance against differential attacks. Dillon et al. has constructed an even S-box for n=6 in 2009. If you can solve this, you can construct one too. Set S=8 and try to solve :)

Many thanks to Ivica Nikolic for the problem description and for interesting discussions.

To generate a set of problems for n=6 that try to re-create Dillon's result:

```
git clone https://github.com/msoos/sbox
cd sbox
git submodule init
git submodule update
./gen_problems.sh
lingeling sbox_problem_36.cnf
```
This should solve in some seconds. It gives 36 of Dillon's 64 s-box settings to the solver, so it won't find a new solution, just re-find the old one. Note that `sbox_problem_35.cnf` is a lot harder. It only gets worse for n=8 -- there is no known solution there... yet.

For more information about almost perfectly non-linear functions, see [here](https://www.ucc.ie/en/media/academic/centreforplanningeducationresearch/FGologlu.pdf) and [here](http://orion.math.iastate.edu/dept/thesisarchive/PHD/MaxwellPhDS05.pdf).

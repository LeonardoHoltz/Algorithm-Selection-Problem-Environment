
# IRace-Environment

This is an environment to use the Irace with the PDPTW using at first the Li & Lim Instances

The target runner is setup to use the irace folder inside the math-pdptw folder.

You need the scenario, parameters, train_instances and the target-runner to use the irace with the pdptw program.

For more further instructions use the irace tutorial: https://cran.r-project.org/web/packages/irace/vignettes/irace-package.pdf


# How do I setup my _irace_ experiment?

The [irace](irace) directory contains an almost-ready-to-run environment to run the automatic algorithm configuration (AAC) experiment for _math-pdptw_ using the _irace_ tool. You only need to follow these steps to be able to run an experiment.

1. Clone the [math-pdptw](https://github.com/cssartori/math-pdptw) repository.
2. Build the solver; You need a copy of CPLEX for that, so ask to your advisor/professor.
3. Download and extract the Li & Lim instance dataset from [SINTEF](https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/); You only need the `pdp 100-case` zip file.
4. Adjust path to the solver, and to the instance files in [scenario.txt](irace/scenario.txt) 

Once you finish these steps, use the terminal to browse to the [irace](irace) directory, then call the `irace` command. In ubuntu-18.04, the command line is the follows.

```bash
$ cd irace
$ /home/alberto/R/x86_64-pc-linux-gnu-library/3.4/irace/bin/irace 
```

After typing this command, `irace` starts the AAC experiment.

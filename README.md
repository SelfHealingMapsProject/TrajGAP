# Knowledge from Incomplete Trajectories: Navigation systems do not cater for familiar wayfinders

Companion demonstration code to the paper.

This code requires Numpy and Pandas, and iPython (jupyter) to run the notebook, tested with versions {Numpy:1.20.2,Pandas:1.2.4} on OSX with Python 3.9.2 (But should work with any Python 3.7+). The attached conda environment trajEnv.yml is provided for those using Anaconda.

You can recreate the environment by issuing the following bash command, issued from within the directory with the following structure:

```
DIR/
|____/data
     |____ gap_trajs_input_data.csv (your input dataset)
     |____ session_annot.csv (expected output dataset)
|____/figs (contains doc figures, may be left out)
     |____ conceptualNeighbourhood.png  
     |____ trajectory_annot.png
|_ gap_trajectories_notebook.ipynb (main executable notebook containing the method)
|_ README.md (this readme)
|_ trajEnv.yml (Conda project environment)

```

The environment was created with the --from-history flag, so should minimize incompatibilities with future versions of the libraries.

You recreate the environent as follows:

```
conda env create -f trajEnv.yml
conda activate trajEnv

```
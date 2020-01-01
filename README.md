- Install environment and packages: (CUDA 10.0)
conda create -n WL python=3.6 -y
source activate WL
conda install numpy matplotlib
conda install -c anaconda tensorflow-gpu

To run file *.jpynb, use this command in terminal: jupyter notebook

- Reference:
https://anaconda.org/anaconda/tensorflow-gpu
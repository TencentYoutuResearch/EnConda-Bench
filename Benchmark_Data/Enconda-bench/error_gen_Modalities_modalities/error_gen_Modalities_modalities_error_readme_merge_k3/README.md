# Modalities

[
![License](https://img.shields.io/badge/License-MIT-blue.svg)
](https://opensource.org/licenses/MIT')
[
![Coverage Status](https://coveralls.io/repos/github/Modalities/modalities/badge.svg)
](https://coveralls.io/github/Modalities/modalities)



# Getting started
For training and evaluation a model, feel free to checkout [this](https://github.com/Modalities/modalities/blob/main/examples/getting_started/getting_started_example.md) getting started tutorial, in which we train a small, 60M-parameter GPT model on a tiny subset of the Redpajama V2 dataset. 
Also, see our Wiki and API reference documentation: https://modalities.github.io/modalities/

# Installation

First, install the repository via


```
pip install -e . 
```

Then, create conda environment and activate it via 

```
conda create -n modalities python=3.10
conda activate modalities


```

If you want to contribute, have a look at `CONTRIBUTING.md`.



# Usage
For running the training endpoint on multiple GPUs run `CUDA_VISIBLE_DEVICES=2,3 torchrun --nproc_per_node 2 --rdzv-endpoint=0.0.0.0:29502 src/modalities/__main__.py run --config_file_path config_files/config.yaml`.



Or, if you are a VsCode user, add this to your `launch.json`:

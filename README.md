## About
The `pepgm-gui` is a web-based user interface that lets you create and modify configuration files, and run PepGM's
Snakemake workflow.

## Prerequisites
Make sure that you have installed the newest Snakemake version:

`snakemake --version`

You can find installing instructions on the [PepGM](https://github.com/BAMeScience/PepGM) GitHub page.

Install the repo using git:

` git clone https://github.com/ziskaki/pepgm-gui/tree/main`

## Preparation
Please follow the instructions [here](https://github.com/BAMeScience/PepGM) for setting up PepGM.
If you have already used PepGM before, you can skip this.
 
Update your conda environment to include the additional packages:

`conda env update --file environment.yml`

## Usage
To start the user interface:

`python3 ui.py`




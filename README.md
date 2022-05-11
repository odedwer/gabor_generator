# Gabor-Patch generator
Generate and save Gabor-patches

## Description
The file within this project generates and saves Gabor patches with different possible envelopes.
Can be used to create a range of orientations with a single command line run.

## Requirements
Python 3 installation with numpy, matplotlib and PIL (pillow) modules installed.

## Usage example
The file should be used from the command line interface (CLI).
To use, download the make_gabor.py file to a folder and run the terminal from that folder.
In the terminal, run 
'''
python make_gabor --help
'''
to view the different options and defaults.

To generate a Gabor-patch with a frequency of 0.1 and orientation of 45 degrees, run
'''
python make_gabor -f 0.1 -o 45
'''

To generate 31 equally spaced orientations between 0 and 90, run
'''
python make_gabor -f 0.1 -o 0 90 --num_orientations=31
'''

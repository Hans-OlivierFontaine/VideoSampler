# VideoSampler
A complete video sampler used to split video files into subset of images according to a sampling frequency
## Installation
Install the various conda libraries in the environment file using:
````
conda env create -f environment.yml
````
## Usage
Run:
````
python VideoSampler.py
````
This can handle the following arguments:
- --source XXX: (Path) The path to the folder containing the videos (must exist)
- --output XXX: (Path) The path to the folder used to output (can be created dynamically)
- --sampling_rate XXX: (integer) The number of frames saved per second (must not exceed actual video fps)
- --workers XXX: (integer) Not implemented yet!
- --directories: If entered, images are stored in subfolders named after the original video instead of directly in the output folder
- --gui: If entered, options are entered through a GUI
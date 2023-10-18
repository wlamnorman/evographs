# Evographs
This repository implements a installable package called `evographs` which implements the spatial Moran model on a Graph class, allows for carrying out simulations and animations of the evolution of a Graph object whose nodes reproduce according to the Moran model.

# Running a simulation 
Running `python3 -m evographs -h` in the terminal while in the root directory and set parameters as per your liking to start a simulation that is then saved as an animated video that visualises the evolution of the population similarly to the video below.

The below animation for example was made using
```python
python3 -m evographs -n_nodes 50 -n_genotypes 16 -edge_probability 0.2 -selection_intensity 0.8
```
<video src="https://github.com/wlamnorman/evographs/assets/71151811/d9e38fa3-c932-4ccd-a213-9921ece91000"></video>


## :beetle: known-bugs :bug:
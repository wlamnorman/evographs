# Evographs
Starting of as a repository to explore algorithms on graphs with the intention of considering how populations evolve over time with a population structure determined by the graph.


# Running a simulation 
Running `python3 -m evographs -h` in the terminal while in the root directory and set parameters as per your liking to start a simulation that is then saved as an animated video that visualises the evolution of the population similarly to the video below.

<video src="https://user-images.githubusercontent.com/71151811/273640700-4d10b6e9-0b33-49d7-839f-d7971c8a9129.mp4"></video>


## :beetle: known-bugs :bug:

## TODO
* Update `MoranModel` class with proper fitness functions based on payoff matrix and selection intensity: use defined functions for fitness calculations to update the `_select_individual` method in `MoranModel`.
* Visualise fitness over generations
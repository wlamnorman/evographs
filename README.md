# Evographs
Starting of as a repository to explore algorithms on graphs with the intention of considering how populations evolve over time with a population structure determined by the graph.

![Evolutionary Graph](https://user-images.githubusercontent.com/71151811/271765284-d7300f23-0707-46d5-8fe8-f2f0fe612066.png)

# Running a simulation 
Running `python3 -m evographs` in the terminal while in the root directory starts a simulation that is then saved as an animated video that visualises the evolution of the population.

## :beetle: known-bugs :bug:

## TODO
* argparse to `__main__.py` to control simulation parameters
Finish `MoranModel` class (coming in v2 of `moran_model.py`) with proper fitness functions based of a payoff matrix
* Proper fitness function based on given payoff matrix and proportion of strategies.
* Visualisation extensions:
    - fitness over generations
    - proportion of strategies over generations.

## Ideas for later development
* Use plotly for graph plots to incorporate connectivity? https://plotly.com/python/network-graphs/
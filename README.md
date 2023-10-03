# Evographs
Starting of as a repository to explore algorithms on graphs with the intention of considering how populations evolve over time with a population structure determined by the graph.

![Evolutionary Graph](https://user-images.githubusercontent.com/71151811/271765284-d7300f23-0707-46d5-8fe8-f2f0fe612066.png)

## TODO
* Fix automatical venv-activation upon opening repository
* Make sure imports are correct and that root of dir is exported
* Solve bug where networkx genotype does not update (how does test not fail??)


## To be implemented
* Visualisation of graph over generations (add generation number value counts visualisation)
* `MoranModel` class
* Proper fitness function based on given payoff matrix and proportion of strategies.
* Visualisation
    - fitness over generations
    - proportion of strategies over generations.

## :beetle: known-bugs :bug:
* When plotting population history from moran model simulations the networkx genotypes do not update properly
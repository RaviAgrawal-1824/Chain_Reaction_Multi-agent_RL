# Chain_Reaction_MARL
The Chain reaction game is controlled using multi-agent RL algorithms.

## Table of Contents
- [Description of game](#description-of-game)
- [Description of Environment](#description-of-environment)
- [Requirements](#requirements)
- [State Space](#state-space)
- [Action Space](#action-space)
- [Reward Function](#reward-function)
- [Algorithms Implemented](#algorithms-implemented)
    - [Tabular Methods](#tabular-methods)
    - [Learning Methods](#learning-methods)
- [Results](#results)

## Description of game

The objective of Chain Reaction is to take control of the board by eliminating your opponents' orbs.

The rules have been described considering two-player (Red and Green) in the game but this could be generalized to any number of players.
For each cell on the board, we define a critical mass. The critical mass is equal to the number of orthogonally adjacent cells. That would be 4 for usual cells, 3 for cells in the edge and 2 for cells in the corner.
All cells are initially empty. Players take turns to place their orbs in a cell. The Red player can only place one (red) orb in an empty cell or a cell that already contains one or more red orbs. When two or more orbs are placed in the same cell, they stack up.
Once a cell has reached critical mass, the stack explodes into the surrounding cells adding an extra orb and claiming the cells for the player. The chain reaction of explosion continues until every cell is stable.
As soon as a player loses all their orbs they are out of the game.
The winner is the one who eliminates every other player's orbs.

|<img src="https://github.com/RaviAgrawal-1824/Chain_reaction_RL/assets/109269344/023be333-b975-4338-9c76-35aa5a980647" width="355" height="592" /> |
|:--:|
|Chain Reaction game shows orbs of multiple players|


## Description of Environment
The chain reaction game is modeled and represented in tabular form in this environment.  
`Score_grid` is of the board size and its value in each grid represents the number of orbs present in each grid.
- 0 - The grid is empty and unoccupied
- 1, 2, 3 - The grid is occupied by any player and has corresponding orbs

`Player_grid` is also of the board size. It contains either 0 or characters A, B, C and so on to represent different players or agents in the game.
- 0 - The grid is empty and unoccupied
- Any character - The grid belongs to that player or agent

|<img src="https://github.com/RaviAgrawal-1824/Chain_reaction_RL/assets/109269344/27836be2-1794-4a9c-aeac-a114a7bc7e5c" width="520" height="590" /> |
|:--:|
|Model of the game showing score grid and player grid|

## Requirements
You don't need any libraries for its implementation as this is developed from scratch. It started by modeling the game and letting the agent take random actions till its termination.
Once the game was working as expected, I began designing the environment which returns current observation, rewards, and termination. Then I made a human mode to play against any human importing class as its testing. Once everything was working as expected, I started training two agents as each other opponents. Once the agents were trained well, I developed a semi-human mode to play against this agent.


## State Space
For all agents to learn in a similar way, I masked the observation for each player. Only 'Player_grid' is changed.
- 0 - The grid is empty and unoccupied
- A - The grid belongs to the agent
- B - The grid belongs to any of the opponents
Score_grid and masked_grid are then flattened and concatenated into 1D tuple for tabular methods.
This tuple is the state space representation for training the agents.  

`Current_State=(flattened score_grid) + (flattened_masked_player-grid)`

## Action Space
The action space depends on the current state and is not generalized for all states. The action space for any state includes all valid actions for the agent in the current state.  
The current state is passed through `available_actions()` which returns all the valid actions for the agent. It returns a list including all (row, col) pairs in the grid that either belongs to the agent or are unoccupied.

## Reward Function
The objective of the agent is to win the game. A small reward is provided when the agent captures the opponent's balls and is proportional to the balls captured. 
- When the agent wins over opponent: +2
- When the agent captures opponent's balls: (balls_captured)/(rows+columns)

The two agents are simultaneously trained with two different Q_lookup tables. Positive reward to one agent and same negative reward to other agent are given. Final Q table is the average of both tables.


## Algorithms Implemented
### Tabular Methods
Tabular Model-Free algorithms are implemented on both agents in this environment like:
- Q-learning
- SARSA-Lambda
- SARSA-Backwards

### Learning Methods
Different MARL methods will be implemented using neural networks to train agent on large scale.

## Results
- Training



- Testing




For more information on this environment, please visit its [Chain_reaction_class](https://github.com/Talendar/flappy-bird-gym).


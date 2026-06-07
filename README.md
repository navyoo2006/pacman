# Project: Pacman

# Description: Implementation of Pacman game.
# Objective:   Reach the finish line of the maze while avoiding the ghost.
#              Collect as much food as possible.
# Basics:
# - Pacman moves from top left to bottom right
# - Every square except for the square of the pacman has a piece of food until eaten by the pacman
# - Ghosts may also occupy squares with food
# - Player loses if a ghost eats the pacman
# - Player wins if bottom right reached
# - Points = pieces of food eaten
# Maze rules per level:
# - Minimum cycle size: (level - 1) // 2 + 5
# - Height: 8 + ((level - 1) // 2) * 2
# - Width: 8 + (level // 2) * 2
# - Ghosts: level // 3 + 1
# Ghost strategies:
# - Move towards pacman in shortest path (DFS)
# - Traverse the entire maze randomly but fast (Kruskal + post-order tree traversal)
# - Move straight across towards correct column and straight up/down towards correct row


## Run Pytest:
- pytest

## To-do:
- [X] Maze generation: Generate a random pacman maze with cycle sizes of at least 6
- [ ] Create and run test suite for DSU, MazeNode and Maze
- [X] Start sprint workflow
- [ ] Set up DJango framework
- [ ] Ghost movement: Efficiently track shortest path continuously with moving targets

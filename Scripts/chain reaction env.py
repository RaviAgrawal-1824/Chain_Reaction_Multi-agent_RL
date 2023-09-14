import random
import numpy as np
import sys
sys.setrecursionlimit(500)

def observation_space(rows,cols):
    score_space_size = 4**2
    score_space_size +=  (2*(rows+cols-4))**3
    score_space_size +=  ((rows*cols)-(2*(rows+cols))+4)**4
    player_space_size = (rows*cols)**3 # could be **2 as for fixed score grid, each cell in player grid could have atmost 2 possibilites.
    state_space_size = score_space_size*player_space_size
    print(f'Box({rows},{cols},2) containing score grid of size {score_space_size} and player grid of size {player_space_size}.')
    print('Total state space size is:',state_space_size)
    return state_space_size

def action_space(rows,cols):
    print('Total action space size is:', (rows*cols))
    return (rows*cols)

def check_winner(check_grid):
    count_a = 0
    count_b = 0

    for r in range(len(check_grid)):
        for c in range(len(check_grid[0])):
            if check_grid[r][c]=='A':
                count_a=count_a+1
            elif check_grid[r][c]=='B':
                count_b=count_b+1

    if count_a == 0:
        print('B won in check winner loop')
        return 'B'
    elif count_b == 0:
        print('A won in check winner loop')
        return 'A'
    else:
        return 0  # No winner yet

def initialize_grid(rows, cols):
    return [[[0 for _ in range(cols)] for _ in range(rows)] for _ in range(2)]

def print_grid(grid):
    print('\nScore_grid')
    for grids in range(len(grid)):
        if grids==1:
            print('\nPlayer_grid')
        for row in grid[grids]:
            print(' '.join(str(cell) for cell in row))
    # print('\nPlayer_grid')

def cal_reward(grid,row,col,player,dirn):
    
    try:
        if grid[player_grid][row-1][col]!=player and dirn=='up' and row >= 0:
            return grid[score_grid][row-1][col]
    except IndexError:
        pass
    try:
        if grid[player_grid][row][col+1]!=player and dirn=='right' and col < len(grid[player_grid][0]):
            return grid[score_grid][row][col+1]
    except IndexError:
        pass
    try:
        if grid[player_grid][row+1][col]!=player and dirn=='down' and row < len(grid[player_grid]) :
            return grid[score_grid][row+1][col]
    except IndexError:
        pass
    try:
        if grid[player_grid][row][col-1]!=player and dirn=='left' and col >= 0:
            return grid[score_grid][row][col-1]
    except IndexError:
        pass

    return 0

def spread_reaction(grid,player,row,col,turn):

    global player_grid, score_grid
    win_val,reward_val=False,0

    if row < 0 or row >= len(grid[player_grid]) or col < 0 or col >= len(grid[player_grid][0]):
        return reward_val,win_val
    
    win=check_winner(grid[player_grid])
    if turn>1 and win==player:
        reward_val=reward_val+10 # winning reward
        return reward_val,True

    if grid[player_grid][row][col]!=player:
        grid[player_grid][row][col] = player
    
    if (row == 0 and col == 0) or (row == len(grid[score_grid]) - 1 and col == len(grid[score_grid][0]) - 1) or (row == len(grid[score_grid]) - 1 and col == 0) or (row == 0 and col == len(grid[score_grid][0]) - 1):

        if grid[score_grid][row][col] >= 1:
            grid[score_grid][row][col] = 0
            grid[player_grid][row][col]= 0

            reward=cal_reward(grid,row,col,player,'up')
            # print(f"$ reward in this up spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val1,win_val1=spread_reaction(grid, player, row - 1, col,turn)
            reward_val= reward_val + reward_val1 + reward
            if win_val1==True:
                return reward_val,win_val1

            reward=cal_reward(grid,row,col,player,'right')
            # print(f"$ reward in this right spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val2,win_val2=spread_reaction(grid, player, row, col + 1,turn)
            reward_val= reward_val + reward_val2 + reward
            if win_val2==True:
                return reward_val,win_val2

            reward=cal_reward(grid,row,col,player,'down')
            # print(f"$ reward in this down spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val3,win_val3=spread_reaction(grid, player, row + 1, col,turn)
            reward_val= reward_val + reward_val3 + reward
            if win_val3==True:
                return reward_val,win_val3

            reward=cal_reward(grid,row,col,player,'left')
            # print(f"$ reward in this left spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val4,win_val4=spread_reaction(grid, player, row, col - 1,turn)
            reward_val= reward_val + reward_val4 + reward
            if win_val4==True:
                return reward_val,win_val4

            win_val = win_val or win_val1 or win_val2 or win_val3 or win_val4
            return reward_val,win_val
        else:
            grid[score_grid][row][col] += 1
            return reward_val,win_val

    elif row == 0 or row == len(grid[score_grid]) - 1 or col == 0 or col == len(grid[score_grid][0]) - 1:

        if grid[score_grid][row][col] >= 2:
            grid[score_grid][row][col] = 0
            grid[player_grid][row][col]= 0

            reward=cal_reward(grid,row,col,player,'up')
            # print(f"$ reward in this up spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val1,win_val1=spread_reaction(grid, player, row - 1, col,turn)
            reward_val= reward_val + reward_val1 + reward
            if win_val1==True:
                return reward_val,win_val1

            reward=cal_reward(grid,row,col,player,'right')
            # print(f"$ reward in this right spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val2,win_val2=spread_reaction(grid, player, row, col + 1,turn)
            reward_val= reward_val + reward_val2 + reward
            if win_val2==True:
                return reward_val,win_val2

            reward=cal_reward(grid,row,col,player,'down')
            # print(f"$ reward in this down spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val3,win_val3=spread_reaction(grid, player, row + 1, col,turn)
            reward_val= reward_val + reward_val3 + reward
            if win_val3==True:
                return reward_val,win_val3

            reward=cal_reward(grid,row,col,player,'left')
            # print(f"$ reward in this left spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val4,win_val4=spread_reaction(grid, player, row, col - 1,turn)
            reward_val= reward_val + reward_val4 + reward
            if win_val4==True:
                return reward_val,win_val4

            win_val = win_val or win_val1 or win_val2 or win_val3 or win_val4
            return reward_val,win_val
        else:
            grid[score_grid][row][col] += 1
            return reward_val,win_val

    elif grid[score_grid][row][col] >= 3:
            grid[score_grid][row][col] = 0
            grid[player_grid][row][col]= 0

            reward=cal_reward(grid,row,col,player,'up')
            # print(f"$ reward in this up spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val1,win_val1=spread_reaction(grid, player, row - 1, col,turn)
            reward_val= reward_val + reward_val1 + reward
            if win_val1==True:
                return reward_val,win_val1

            reward=cal_reward(grid,row,col,player,'right')
            # print(f"$ reward in this right spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val2,win_val2=spread_reaction(grid, player, row, col + 1,turn)
            reward_val= reward_val + reward_val2 + reward
            if win_val2==True:
                return reward_val,win_val2

            reward=cal_reward(grid,row,col,player,'down')
            # print(f"$ reward in this down spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val3,win_val3=spread_reaction(grid, player, row + 1, col,turn)
            reward_val= reward_val + reward_val3 + reward
            if win_val3==True:
                return reward_val,win_val3

            reward=cal_reward(grid,row,col,player,'left')
            # print(f"$ reward in this left spread at ({row+1},{col+1}) in turn {turn} by {player}:{reward}")
            reward_val4,win_val4=spread_reaction(grid, player, row, col - 1,turn)
            reward_val= reward_val + reward_val4 + reward
            if win_val4==True:
                return reward_val,win_val4
            win_val = win_val or win_val1 or win_val2 or win_val3 or win_val4
            return reward_val,win_val

    else:
        grid[score_grid][row][col] += 1
        return reward_val,win_val

def step(action):
    pass
    global score_grid,player_grid,grid

    # reward_val,win_val = spread_reaction(grid, player, action[0], action[1],turn)

def play():

    players_name = ['A','B']
    player_index = 1

    for turn in range(turns):
        print('-'*50)

        player_index = (player_index + 1) % 2
        player = players_name[player_index]
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        while grid[player_grid][row][col] != player and grid[player_grid][row][col] !=0:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)

        print(f"Player {player} triggered reaction at ({row+1}, {col+1})")
        reward_val,win_val = spread_reaction(grid, player, row, col,turn)
        # print(f'rewards obtained is {reward_val} and win value is {win_val} in the play count {turn}.')
        # print('win value is', win_val,'and play count is',turn)
        print_grid(grid)
        # print(reward_val,win_val)

        if win_val:
            print('Game Finished'+' '+'*'*50+' '+player +' won the game')
            sys.exit()

if __name__ == "__main__":
    score_grid,player_grid=0,1
    rows,cols = 4,4
    turns=60
    grid = initialize_grid(rows, cols)
    observation_space(rows,cols)
    action_space(rows,cols)
    play()
  
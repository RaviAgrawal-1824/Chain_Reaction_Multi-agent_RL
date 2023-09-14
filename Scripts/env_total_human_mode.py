from env_making_class import *
import numpy as np
import pickle


def mask_env(obj):
    masked_grid=[[0 for _ in range(obj.cols)] for _ in range(obj.rows)]
    for r in range(obj.rows):
        for c in range(obj.cols):
            if obj.player_grid[r][c]==obj.player:
                masked_grid[r][c]=1
            elif obj.player_grid[r][c]==0:
                masked_grid[r][c]=0
            else:
                masked_grid[r][c]=2
    masked_grid=np.concatenate(((np.array(obj.score_grid).flatten()),(np.array(masked_grid).flatten())))
    return(tuple(masked_grid))

def available_action(obj):
    action_allowed=[]
    for r in range(obj.rows):
        for c in range(obj.cols):
            if obj.player_grid[r][c]==obj.player or obj.player_grid[r][c]==0:
                action_allowed.append((r,c))
    return(action_allowed)

game=chain_reaction_v0(3,3)
Q_lookup={}

# with open('my_dict.pkl', 'rb') as f:
#     Q_lookup = pickle.load(f)

turns=30
for turn in range(turns):


    game.player_index = (game.player_index + 1) % 2
    game.player = game.players_name[game.player_index]

    print('-'*50)
    print(f'Please play your turn as player {game.player}:')
    row=int(input('Row:'))
    col=int(input('Col:'))
    if (row,col) in available_action(game):
        obs,reward,done = game.step((row, col))
    else:
        print('invalid action')
        continue
    
    print(f"\nPlayer {game.player} triggered reaction at ({row+1}, {col+1})")
    print()
    game.print_grid()
    print(f'\nrewards obtained is {game.reward} and win value is {done} in the play count {turn}.')


    if game.win or done:
        print('Game Finished'+' '+'*'*50+' '+game.player +' won the game')
        sys.exit()
# import sys
# import random

class chain_reaction_v0:

    
    def __init__(self,rows=3,cols=3,p1='A',p2='B') -> None:
        self.rows=rows 
        self.cols=cols
        self.grid=[[[0 for _ in range(cols)] for _ in range(rows)] for _ in range(2)]
        self.score_grid=self.grid[0]
        self.player_grid=self.grid[1]
        self.turn=0
        
        self.reward_a=0
        self.reward=0
        self.reward_b=0
        self.win=False
        self.players_name=[p1,p2]
        self.player_index=1
        self.player=self.players_name[self.player_index]

        pass
    
    def step(self,action):
        self.reward,self.win=0,False
        self.reward_a,self.reward_b=0,0
        self.reward,self.win=self.spread_reaction(action[0],action[1])
        self.reward=self.reward/(self.rows + self.cols)
        if self.win==True:
            self.reward=self.reward+2
            # self.print_grid()
            # print('action',action,'player is',self.player)
            # print('turn is',self.turn,'reward is',self.reward,'win is',self.win,'player is',self.player)
        if self.player_index==0:
            self.reward_a=self.reward
            self.reward_b=-1*self.reward
        else:
            self.reward_b=self.reward
            self.reward_a=-1*self.reward
        return (self.score_grid+self.player_grid),self.reward,self.win

    def check_winner(self):
        count_a = 0
        count_b = 0

        for r in self.player_grid:
            for c in range(len(r)):
                if r[c]==self.players_name[0]:
                    count_a=count_a+1
                elif r[c]==self.players_name[1]:
                    count_b=count_b+1

        if count_a == 0 and count_b>1:
            # print('player 2 won in check winner loop')
            return self.players_name[1]
        elif count_b == 0 and count_a>1:
            # print('player 1 won in check winner loop')
            return self.players_name[0]
        else:
            return 0  # No winner yet

    def spread_reaction(self,row,col):

        # global player_grid, score_grid
        win_val,reward_val=False,0

        if row < 0 or row >= len(self.player_grid) or col < 0 or col >= len(self.player_grid[0]):
            return reward_val,win_val
        
        win=self.check_winner()
        if win==self.player:
            return reward_val,True
        elif win!=0:
            # print('$'*30)
            # print('check winner shows someone won but it is not the agent.')
            # self.print_grid()
            # print('action',(row,col),'player is',self.player)
            # print('turn is',self.turn,'reward is',self.reward,'win is',win)
            # sys.exit()
            pass

        if self.player_grid[row][col]!=self.player:
            self.player_grid[row][col] = self.player
        
        if (row == 0 and col == 0) or (row == len(self.score_grid) - 1 and col == len(self.score_grid[0]) - 1) or (row == len(self.score_grid) - 1 and col == 0) or (row == 0 and col == len(self.score_grid[0]) - 1):

            if self.score_grid[row][col] >= 1:
                self.score_grid[row][col] = 0
                self.player_grid[row][col]= 0

                reward=self.cal_reward(row,col,'up')
                # print(f"$ reward in this up spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val1,win_val1=self.spread_reaction(row - 1, col)
                reward_val= reward_val + reward_val1 + reward
                if win_val1==True:
                    return reward_val,win_val1

                reward=self.cal_reward(row,col,'right')
                # print(f"$ reward in this right spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val2,win_val2=self.spread_reaction(row, col + 1)
                reward_val= reward_val + reward_val2 + reward
                if win_val2==True:
                    return reward_val,win_val2

                reward=self.cal_reward(row,col,'down')
                # print(f"$ reward in this down spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val3,win_val3=self.spread_reaction(row + 1, col)
                reward_val= reward_val + reward_val3 + reward
                if win_val3==True:
                    return reward_val,win_val3

                reward=self.cal_reward(row,col,'left')
                # print(f"$ reward in this left spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val4,win_val4=self.spread_reaction(row, col - 1)
                reward_val= reward_val + reward_val4 + reward
                if win_val4==True:
                    return reward_val,win_val4

                win_val = win_val or win_val1 or win_val2 or win_val3 or win_val4
                return reward_val,win_val
            else:
                self.score_grid[row][col] += 1
                win=self.check_winner()
                if win == self.player:
                    return reward_val, True
                return reward_val,win_val

        elif row == 0 or row == len(self.score_grid) - 1 or col == 0 or col == len(self.score_grid[0]) - 1:

            if self.score_grid[row][col] >= 2:
                self.score_grid[row][col] = 0
                self.player_grid[row][col]= 0

                reward=self.cal_reward(row,col,'up')
                # print(f"$ reward in this up spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val1,win_val1=self.spread_reaction(row - 1, col)
                reward_val= reward_val + reward_val1 + reward
                if win_val1==True:
                    return reward_val,win_val1

                reward=self.cal_reward(row,col,'right')
                # print(f"$ reward in this right spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val2,win_val2=self.spread_reaction(row, col + 1)
                reward_val= reward_val + reward_val2 + reward
                if win_val2==True:
                    return reward_val,win_val2

                reward=self.cal_reward(row,col,'down')
                # print(f"$ reward in this down spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val3,win_val3=self.spread_reaction(row + 1, col)
                reward_val= reward_val + reward_val3 + reward
                if win_val3==True:
                    return reward_val,win_val3

                reward=self.cal_reward(row,col,'left')
                # print(f"$ reward in this left spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val4,win_val4=self.spread_reaction(row, col - 1)
                reward_val= reward_val + reward_val4 + reward
                if win_val4==True:
                    return reward_val,win_val4

                win_val = win_val or win_val1 or win_val2 or win_val3 or win_val4
                return reward_val,win_val
            else:
                self.score_grid[row][col] += 1
                win=self.check_winner()
                if win == self.player:
                    return reward_val, True
                return reward_val,win_val

        elif self.score_grid[row][col] >= 3:
                self.score_grid[row][col] = 0
                self.player_grid[row][col]= 0

                reward=self.cal_reward(row,col,'up')
                # print(f"$ reward in this up spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val1,win_val1=self.spread_reaction(row - 1, col)
                reward_val= reward_val + reward_val1 + reward
                if win_val1==True:
                    return reward_val,win_val1

                reward=self.cal_reward(row,col,'right')
                # print(f"$ reward in this right spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val2,win_val2=self.spread_reaction(row, col + 1)
                reward_val= reward_val + reward_val2 + reward
                if win_val2==True:
                    return reward_val,win_val2

                reward=self.cal_reward(row,col,'down')
                # print(f"$ reward in this down spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val3,win_val3=self.spread_reaction(row + 1, col)
                reward_val= reward_val + reward_val3 + reward
                if win_val3==True:
                    return reward_val,win_val3

                reward=self.cal_reward(row,col,'left')
                # print(f"$ reward in this left spread at ({row+1},{col+1}) in turn {turn} by {self.player}:{reward}")
                reward_val4,win_val4=self.spread_reaction(row, col - 1)
                reward_val= reward_val + reward_val4 + reward
                if win_val4==True:
                    return reward_val,win_val4
                win_val = win_val or win_val1 or win_val2 or win_val3 or win_val4
                return reward_val,win_val

        else:
            self.score_grid[row][col] += 1
            win=self.check_winner()
            if win == self.player:
                return reward_val, True
            return reward_val,win_val

    def print_grid(self):
            for row in self.score_grid:
                print(' '.join(str(cell) for cell in row))
            print('-----')
            for row in self.player_grid:
                print(' '.join(str(cell) for cell in row))
            # print()

    def cal_reward(self,row,col,dirn):
        
        try:
            if self.player_grid[row-1][col]!=self.player and dirn=='up' and row >= 0:
                return self.score_grid[row-1][col]
        except IndexError:
            pass
        try:
            if self.player_grid[row][col+1]!=self.player and dirn=='right' and col < len(self.player_grid   [0]):
                return self.score_grid[row][col+1]
        except IndexError:
            pass
        try:
            if self.player_grid[row+1][col]!=self.player and dirn=='down' and row < len(self.player_grid) :
                return self.score_grid[row+1][col]
        except IndexError:
            pass
        try:
            if self.player_grid[row][col-1]!=self.player and dirn=='left' and col >= 0:
                return self.score_grid[row][col-1]
        except IndexError:
            pass

        return 0

    def observation_space(self):
        score_space_size = 4**2
        score_space_size +=  (2*(self.rows+self.cols-4))**3
        score_space_size +=  ((self.rows*self.cols)-(2*(self.rows+self.cols))+4)**4
        player_space_size = (self.rows*self.cols)**3 # could be **2 as for fixed score grid, each cell in player grid could have atmost 2 possibilites.
        state_space_size = score_space_size*player_space_size
        print(f'Box({self.rows},{self.cols},2) containing score grid of size {score_space_size} and player grid of size {player_space_size}.')
        print('Total state space size is:',state_space_size)
        return state_space_size
    
    def action_space(self):
        print('Total action space size is:', (self.rows*self.cols))
        return (self.rows*self.cols)

    def reset(self):
        self.grid=[[[0 for _ in range(self.cols)] for _ in range(self.rows)] for _ in range(2)]
        self.score_grid=[[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.player_grid=[[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.turn=0
        self.reward_a=0
        self.reward=0
        self.reward_b=0
        self.win=False
        self.player_index=1
        self.player=self.players_name[self.player_index]
        return self.grid



















# game=chain_reaction_v0(6,6)
# turns=80
# for turn in range(turns):
#     print('-'*50)

#     game.player_index = (game.player_index + 1) % 2
#     game.player = game.players_name[game.player_index]
#     row = random.randint(0, game.rows - 1)
#     col = random.randint(0, game.cols - 1)

#     while game.player_grid[row][col] != game.player and game.player_grid[row][col] !=0:
#         row = random.randint(0, game.rows - 1)
#         col = random.randint(0, game.cols - 1)

#     print(f"Player {game.player} triggered reaction at ({row+1}, {col+1})")
#     game.grid,reward_val,win_val = game.step((row, col))
#     print(f'rewards obtained is {reward_val} and win value is {win_val} in the play count {turn}.')
#     # print('win value is', win_val,'and play count is',turn)
#     game.print_grid()
#     # print(reward_val,win_val)

#     if win_val:
#         print('Game Finished'+' '+'*'*50+' '+game.player +' won the game')
#         sys.exit()
    

from env_making_class import *
import numpy as np 
import random
import matplotlib.pyplot as plt
import pickle
import sys

def mask_env1(obj):
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

def union_dicts_with_average(dict1, dict2):
    result_dict = {}

    all_keys = set(dict1.keys()) | set(dict2.keys())

    for key in all_keys:
        value1 = dict1.get(key)
        value2 = dict2.get(key)

        if value1 is not None and value2 is not None:
            if isinstance(value1, dict) and isinstance(value2, dict):
                # Recursively calculate the union with average for nested dictionaries
                result_dict[key] = union_dicts_with_average(value1, value2)
            else:
                # Calculate the average for numeric values
                result_dict[key] = (value1 + value2) / 2
        elif value1 is not None:
            result_dict[key] = value1
        else:
            result_dict[key] = value2

    return result_dict

# updating both table at each play, need to store prev and new pos for both a and b

env = chain_reaction_v0(3,3)
env.reset()
iteration_list,epoch_list,reward_list=[],[],[]
Q_lookup_A={}  
Q_lookup_B={}  

gamma= 0.7
alpha=1/15  # step size can be reduced further
Lambda=0.9
epsilon=1

max_epoch,min_epoch=800000,0
# max_epoch,min_epoch=8000,0

def update(prev_pos,new_pos,action,imm_reward,Q_table):
    Qval_max = max(list(Q_table[new_pos].values()))
    change = (imm_reward+gamma*Qval_max) - Q_table[prev_pos][action]
    Q_table[prev_pos][action]=Q_table[prev_pos][action]+alpha*change

k,n=0,0
for i in range(min_epoch,int(max_epoch*1.05)):

    epoch_list.append(i+min_epoch)
    done,env.turn,reward=0,1,0
    prev_act=(0,0)
    # punish
    obs=env.reset()
    new_pos=mask_env1(env)
    prev_pos_play=mask_env1(env)
    new_pos_play=mask_env1(env)
    if i%1000==0:
        print('--'*50,'\n',i,'epoch')

    if(i>0 and i<max_epoch+1):
        epsilon=1-i/max_epoch

    # env.player_index = (env.player_index + 1) % 2
    # env.player = env.players_name[env.player_index]
    # if(i>(min_epoch/3) and i<max_epoch*1.1 and i%7==0):
    #     print(Q_lookup)

    while(env.turn<70 and not done):

        env.player_index = (env.player_index + 1) % 2
        env.player = env.players_name[env.player_index]
        if env.player_index==0:
            Q_lookup=Q_lookup_A
        else:
            Q_lookup=Q_lookup_B

        prev_pos=mask_env1(env)
        actions=available_action(env)

        if (not prev_pos in Q_lookup):
            Q_lookup[prev_pos]={element: 0 for element in actions}

        prob_decider=random.uniform(0,1)  # mechanism for choosing action greedily or randomly controlled by epsilon.
        if(epsilon>=prob_decider):
            act=random.choice(actions)
        else:
            act=max(Q_lookup[prev_pos], key=Q_lookup[prev_pos].get) # conversion of dict.values() in list is important for correct greddy action selection.

        try:
            obs,reward,done=env.step(act)  # taking a step in the environment
        except RecursionError:
            print('RecursionError','&'*50)
            print('prev pos',prev_pos,'and player is: ',env.player)
            print('available actions',actions)
            print('action',act,'player is',env.player)
            print('turn is',env.turn,'reward is',env.reward,'win is',done)
            env.print_grid()
            sys.exit()

            # print('turn is',env.turn,'reward is',env.reward,'win is',win)


        new_pos=mask_env1(env)
        actions=available_action(env)

        # print(f'action is {act}, obs is {obs}, reward is {reward}, done is {done}')
        # print('new pos',new_pos,'and player is: ',env.player)
        # print('available actions',actions)
        
        if (not new_pos in Q_lookup):
            Q_lookup[new_pos]={element: 0 for element in actions}

        try:
            if env.player_index==0:
                update(prev_pos,new_pos,act,env.reward_a,Q_lookup_A)
                update(prev_pos_play,new_pos_play,prev_act,env.reward_b,Q_lookup_B)
            else:
                update(prev_pos,new_pos,act,env.reward_b,Q_lookup_B)
                update(prev_pos_play,new_pos_play,prev_act,env.reward_a,Q_lookup_A)
        except KeyError:
            # print('got KeyError')
            pass

        # print('action ',act,'in turn ',env.turn,'and reward A is',env.reward_a,'and reward B is',env.reward_b)

        # update(prev_pos,new_pos,act,reward,Q_lookup)
        prev_pos_play=prev_pos
        new_pos_play=new_pos
        prev_act=act
        # print()
        # env.print_grid()
        # print()

        env.turn=env.turn+1
    iteration_list.append(env.turn)
    reward_list.append(reward)


Q_lookup=union_dicts_with_average(Q_lookup_A,Q_lookup_B)

# with open('dict_A.pkl', 'wb') as f:
#     pickle.dump(Q_lookup_A, f)
# with open('dict_B.pkl', 'wb') as f:
#     pickle.dump(Q_lookup_B, f)
# with open('dict.pkl', 'wb') as f:
#     pickle.dump(Q_lookup, f)


# print(Q_lookup,'\n\n',epoch_list,'\n\n',reward_list,'\n\n',iteration_list)
# x = np.arange(len(reward_list))
plt.plot(reward_list)
plt.xlabel('No. of Epochs')
plt.ylabel('Reward Function')
plt.title('Q-learning applied on chain_reaction_v0')
plt.show()
plt.plot(iteration_list)
plt.xlabel('No. of Epochs')
plt.ylabel('No. of plays taken')
plt.title('Q-learning applied on chain_reaction_v0')
plt.show()












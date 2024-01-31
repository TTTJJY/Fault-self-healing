from random import random, choices
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


M = 40
N = 100
K = 4000
P = 50
Max_num = int(1e6)

class Agent:
    def __init__(self, Max_num):
        self.K = K
        self.M = M
        self.N = N
        self.alpha = 1e-1
        self.gamma = 0.75
        self.beta_min = 1
        self.beta_max = 20
        self.beta = self.beta_min
        self.activities = None
        self.n = np.ones((K,)) # parameter vector
        self.weights = np.random.normal(0, np.sqrt(2/N), (K, N)) # w_kj
        self.intens = np.random.normal(0, np.sqrt(2/K), (M, K)) # u_j
        self.sigmoid = lambda x: 1/(1+np.exp(-x))
        self.Max_num = Max_num
        # SARSA Variables
        self.current_state = None
        self.current_action = None
        self.rwd = None
        self.next_state = None
        self.next_action = None
        self.t = 0
        
    def update(self, sarsa):
        # read state transition
        self.current_state, self.current_action, self.rwd, self.next_state, self.next_action = sarsa
        # perform gradient descent step
        self.Step_gd()
        self.t += 1
        self.Update_beta()
    
    def Update_beta(self):

        self.beta = self.t*(self.beta_max - self.beta_min)/self.Max_num + self.beta_min
        # print(self.beta)
    
    def Step_gd(self):
       
        grad_1 = (self.rwd + self.gamma*self.Approx(self.next_state, self.next_action) -\
                self.Approx(self.current_state, self.current_action))
        features = self.Activities(self.current_state)*((self.intens.T).dot(self.current_action))



        gradient = features * grad_1 # vector gradient
        self.n *= (1 + self.alpha*gradient)
        # repair
        self.n[self.n < 0] = 0
        
    def policy(self, state):
        action = np.zeros((M,))
        probs = self.sigmoid(self.beta*self.intens.dot(self.Activities(state) * self.n))
        thresholds = np.random.rand(M)
        action[thresholds < probs] = 1
        return action
    
    def Activities(self, state):
        # Return cytokine for each cell type k
        return  self.sigmoid(self.weights.dot(state.T))
    
    def Approx(self, state, action):

        features = self.Activities(state)*((self.intens.T).dot(action))
        #print(features.shape)
        q_approx = self.n.dot(features)
        #print("Features", type(features))
        return q_approx
    
    def activity(self, k, state):

        stimulus = self.weights[k].dot(state)
        return self.sigmoid(stimulus)
    

class Environment:
    def __init__(self):
        self.N = N # state space size
        self.M = M # action space size
        self.Pi = Pi # aize of antigen pattern set (state db)
        self.q = .9 # get sick probability
        self.R0 = M/2 # reward threshold
        self.state_db, self.best_act_db = self._gen_db() # states and best actions
        # keys are strings, values are np.array
        self.st_ix = None # current state index
        self.st = None # current state
        self.act = None # action at current state
        self.rwd = None # current reward
   
    def Initial(self):
        ran_ix = int(random()*self.Pi)
        self.st_ix = ran_ix
        self.st = np.ravel(self.state_db[ran_ix])
        return np.ravel(self.state_db[ran_ix]), ran_ix
   
    def update(self, action):

        # compute reward
        self.rwd = self.Reward(self.st_ix, action)
        # generate transition probs
        probs = [self._transition_probs(ixs, action) for ixs in range(len(self.state_db))]
        # select new state
        new_state_ix = choices(range(Pi), probs, k=1)[0]
        self.st_ix = new_state_ix
        self.st = np.ravel(self.state_db[new_state_ix])
        return self.rwd, self.st, self.st_ix
    
    def Gen(self):
        count = 0
        db = {}
        while not len(db) == Pi:
            phato = np.zeros((N))
            probs = np.random.rand(len(phato))
            phato[probs < 0.5] = 1
            db[str(phato)] = phato
            count += 1
        db = np.array(list(db.values()))
        
        best_acts = np.zeros((Pi, M))
        probs = np.random.rand(*best_acts.shape)
        best_acts[probs < 0.5] = 1
      
        return db, best_acts

        
    def Reward(self, state_ix, action):

        return self.M - self.Hamming(np.ravel(self.best_act_db[state_ix]), action) 
    
    def Hamming(self, v_1, v_2):

        return np.sum(np.abs(v_1 - v_2))
    
    def transition(self, target_ix, action):

        if self.st_ix == 0: # if healthy
            if target_ix == 0:
                return 1 - self.q
            else:
                return self.q/(self.Pi-1)
        elif self.st_ix == target_ix:
            prob = (self.M - self.Reward(self.st_ix, action))/(self.M - self.R0)
            return min(1, prob)
        elif target_ix == 0:
            prob = -(self.R0 - self.Reward(self.st_ix, action))/(self.M - self.R0)
            return max(0,prob)
        else:
            return 0.

class Self_healing:
    def __init__(self):
        self.Max_num = Max_num
        self.env = Environment()
        self.agent = Agent(self.Max_num)
        # Histories
        self.s_hist = [] # states
        self.si_hist = [] # state indices 
        self.a_hist = [] # actions 
        self.r_hist = [] # rwds
        
    def run(self):
        next_state, next_state_i, next_action = None, None, None
        for t in range(self.Max_num):
            if t == 0:
                current_state, current_state_i = self.env.initial_state()
                # Agent reads state, responds
                current_action = self.agent.policy(current_state)
            else:
                current_state = next_state
                current_state_i = next_state_i
                current_action = next_action
            self.s_hist.append(current_state)
            self.si_hist.append(current_state_i)
            self.a_hist.append(current_action)
            # Agent reads state, responds
            current_reward, next_state, next_state_i = \
                self.env.update(current_action)
            self.r_hist.append(current_reward)
            next_action = self.agent.policy(next_state)
            # Perform Update
            SARSA = (current_state, current_action, current_reward, next_state, next_action)
            self.agent.update(SARSA)
            # if t % 100 == 0:
                # print(t)
            
            




if __name__ == '__main__':
    model = Self_healing()
    model.run()
    r_hist = model.r_hist[:]
    n = model.agent.n

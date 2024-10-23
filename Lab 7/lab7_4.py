import numpy as np
import matplotlib.pyplot as plt

class NonStationaryBandit:
    def _init_(self, n_arms=10, mean_initial=0.0, std_walk=0.01):
        
        self.n_arms = n_arms
        self.mean_rewards = np.full(n_arms, mean_initial)  
        self.std_walk = std_walk

    def step(self):
        self.mean_rewards += np.random.normal(0, self.std_walk, self.n_arms)

    def pull(self, action):
        true_mean = self.mean_rewards[action]
        reward = np.random.normal(true_mean, 1)  
        return reward

class EpsilonGreedyAgent:
    def _init_(self, n_arms=10, epsilon=0.1, alpha=0.1):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.alpha = alpha 
        self.q_estimates = np.zeros(n_arms) 
        self.action_counts = np.zeros(n_arms)  

    def select_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.n_arms) 
        else:
            return np.argmax(self.q_estimates)  

    def update_estimate(self, action, reward):
        self.q_estimates[action] += self.alpha * (reward - self.q_estimates[action])

def run_experiment(n_steps=10000, epsilon=0.1, alpha=0.1, std_walk=0.01):
    bandit = NonStationaryBandit(n_arms=10, mean_initial=0.0, std_walk=std_walk)
    agent = EpsilonGreedyAgent(n_arms=10, epsilon=epsilon, alpha=alpha)

    rewards = np.zeros(n_steps)  
    actions = np.zeros(n_steps, dtype=int)  

    for t in range(n_steps):
        action = agent.select_action()  
        reward = bandit.pull(action) 
        agent.update_estimate(action, reward) 

        rewards[t] = reward 
        actions[t] = action  

        bandit.step()  

    return rewards, actions

rewards, actions = run_experiment(n_steps=10000, epsilon=0.1, alpha=0.1, std_walk=0.01)


plt.figure(figsize=(10, 5))
plt.plot(np.cumsum(rewards), label='Cumulative Reward')
plt.xlabel('Steps')
plt.ylabel('Cumulative Reward')
plt.title('Cumulative Reward over Time (Modified Epsilon-Greedy)')
plt.legend()
plt.show()

plt.figure(figsize=(10, 5))
plt.hist(actions, bins=np.arange(11) - 0.5, rwidth=0.8, edgecolor='black')
plt.xticks(range(10))
plt.xlabel('Arm')
plt.ylabel('Number of Times Pulled')
plt.title('Distribution of Actions Taken')
plt.show()
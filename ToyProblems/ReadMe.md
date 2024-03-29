I want to experiment with toy problems that are simpler than reward design for 3-sisters. This folder is dedicated to such problems.

# Problem1
Consider single  cell and solve temporal constraints between corn and bean

## formulation
- Environment: single cell with state as 2 x 1 vector, first value representing corn and second value bean.
- ActionSpace: When first value is 0, we have 2 possible actions plant corn or leave empty. Similarly for second value for bean. Note that action space is a function of state space (i.e., available actions change with current state).
- Reward: Bean when planted after a few days of corn will have higher reward. Corn with bean will have higher reward.
  - Bean must be planted after 4-6 days Corn is planted to get the growth from corn. The question was whether agent learns this and plants bean a little late.
- Question: Can an agent learn the above temporal constraint?
  - Start with simple Q-Learning Tabular agent (because the action space and state space is small)

## Observations / Issues
### Iteration (1) : State is a 2-value field (represents whether corn/bean is planted)
- As of now, here are some observations (will improve this section over time):
  - One key question was whether agent figures out planting bean at the right time - so far in any of reward combinations, I couldn't make the agent learn this trick!!! This will be the most interesting insight if proved properly : In RL setting, if there is a situation where for the same (state, action) combination, there is a certain time step in horizon that yields the best reward, can the existing algorithms learn such a phenomenon?
    - Theoritically above makes sense : We cannot expect agent to learn a behavior that depends on 'age' of corn without including 'age' as part of state. At the least we should perhaps treat this problem as a POMDP. ('age' of corn is part of hidden state) , Need to see how tabular Q-learning can be extended to deal with POMDPs (function approaximation is ceratinly one way)
  - When corn without bean has a high reward than corn with bean, agent never plants bean.

### Iteration (2) : State is a 3-value field (include age of corn as part of the state)
- This is in theory supposed to learn planting bean at right time, though there are some runs where this was indeed learnt, the training is too fragile and too random.
  - I got the result so far in only one specific combination (1000 epochs, 0.1 constant learning rate, planting bean early gives a negative reward as well)
  - If I train for 5000 epochs the same combination above, the result no more holds, indeed the agent does not plant anything at any time step at all. Looking closely at Q-table after training, the value of not planting anything on day 0 [(0,0,0), (0,0)] is usually very close to value of planting corn [(0,0,0), (1,0)] and depending on how training goes, if the value of former is slightly higher than later, the agent does not plant anything.
  - One question I asked myself is why try exploiting at all during training time? Sampling random actions at training should in theory evaluate all states equally and well - however this was not the case. Thinking about it, the state distribution is not uniform, the state (0,0,0) [nothing is planted] has a high likelyhood of occurence if we sample actions uniformly and so it gets updated a lot more often. This increases the likelyhood of issue explained above - not planting anything will have a slightly higher value than planting corn and agent does not plant anything at test time. So, I completely discarded this idea.
  - Even then, the agent plants bean either 1 or 2 steps ahead of the right timing. Why is this so? The following is a likely explanation; Below is representation of state diagram in this formulation:
  ![](State_Transitions.JPG)
  The * represents the transaction of high value, when bean is planted through that transaction, we would expect to see a higher return. However, from the reward structure and how value updates are done in Q-learning, the value of state (1,1, 4) [which should have a high value] is not only backed up to (1,0,3) but also to (1,1,3). This is because of bootstrapping (in RL, bootstrapping is updating value function of current state from estimated values of next states).
  - An obvious way to avoid this problem is to give a high reward at the time step when agent plants bean at the right time relative to other time steps (I tried it quickly to validate and that's shown in results too). In this reward setting agent learns to plant the bean at the right time. However, in a way this is directly encoding the policy in the reward design (just return rewards such that best actions get best reward).
  - Another question that would be interesting to explore is to see how using only sparse reward (reward at the end of episode) OR monte carlo methods (that avoid bootstrapping) deals with this problem setup. That would be the next iteration.

### Iteration (3) : Sparse rewards, monte carlo agent
- In this iteration, I implemented an option to choose a sparse reward instead of dense reward i.e., the reward is given only at the end of episode (harvest period). If nothing is planted, the end of episode reward is 0, if only corn is planted, it's 1.0 and only if bean is planted at the right time (which is during certain age of corn) the reward is 2.0. 
- I also implemented a monte carlo sampling based agent (which does not use bootstrapping), this was a little harder than I thought (the open ai gym interfaces as they are defined doesn't seem to support writing code for this agent directly, I had to extend my environment with special methods to build this agent).
- I ran the experiments with QLearning agent and sparse rewards and from those experiments, it was relatively easier to understand the Q-table values and thus agent behavior (than using a dense reward). The training was similar in the sense that it was fragile but works some times. So I did not thing sparse rewards caused more difficulty compared to dense rewards in training the agent (at least for the toy problem).
- Then I ran monte carlo agent with sparse rewards only and as I was expecting this was more reliable in learning the right strategy for the designed toy problem. I could reproduce the results of desired behavior more often (though there is still some randomness some times), note that I only tried at most 2000 epochs in this setup whereas I have tried uptp 5000 epochs on other set ups. Even with 2000 epochs, I was able to get the desired results almost quite often. (greater than 75% of times).

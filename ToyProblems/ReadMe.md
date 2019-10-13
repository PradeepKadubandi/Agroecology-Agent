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
- As of now, here are some observations (will improve this section over time):
  - One key question was whether agent figures out planting bean at the right time - so far in any of reward combinations, I couldn't make the agent learn this trick!!! This will be the most interesting insight if proved properly : In RL setting, if there is a situation where for the same (state, action) combination, there is a certain time step in horizon that yields the best reward, can the existing algorithms learn such a phenomenon?
    - Theoritically above makes sense : We cannot expect agent to learn a behavior that depends on 'age' of corn without including 'age' as part of state. At the least we should perhaps treat this problem as a POMDP. ('age' of corn is part of hidden state) , Need to see how tabular Q-learning can be extended to deal with POMDPs (function approaximation is ceratinly one way)
  - When corn without bean has a high reward than corn with bean, agent never plants bean.

# Big question?
- Can we build an intelligent agent that can learn an effective strategy for growing a polyculture farm ? (using only trial and error i.e., without knowledge of how farms grow)  

## Problem break up
1. Can the agent learn a specific strategy like 3-sisters? 
2. Can the agent generalize well across different such strategies? (For example, can an agent trained against environment that models 3-sisters type reward structure, still make effective decisions for some other plant types / layout?)

Briefly, the simulator effort we are doing is an attempt to build models of farm growth and yield from first principles and once we have the simulator built, we will have good data generating mechanisms in place which enables us to tackle the second problem (generalization). For now, we will focus on first problem (learning a specific strategy) and to focus our efforts further, we will choose 3-sisters as the target strategy that we want to see if our agent can learn.

## A brief primer on 3-sisters
3-sisters is a method that plants corn, bean and squash together in a farm to maximize the total yield while reducing the resources spent. Each plant has some strenth to support others and needs something else from other two:
- Corn:
  - High yield (compared to other plants)
  - Grows straight up (so offers bean the support to swirl around itself)
  - Needs high amount of water and nitrogen (squahsh and corn respectively play a part here)
- Bean
  - It can produce nitrogen (and it produces a little more than it needs which is useful to other two)
  - It needs a pole like structure to twist around and grow on (which corn provides)
- Squash
  - It provides ground cover (prevents evaporation of water and prevents weeds)

One possible approach towards validating this would be to introduce hyper parameters in the modelling to represent : fertilizer and herbicide:
- if fertilizer costs zero, planting corn all over should give the maximum yield, however when fertlizer costs more, planting bean in addition to corn should be better.
- if herbicide costs zero, there is no need for planting squash, however if herbicide costs more, planting squash should be a better strategy.

# General Reinforcement Learning Setup
![](RL.png)

Note that the 'Environment' encapsulates information about how state transitions work OR how much reward is given at each time step. Agent does not know these details, agent only knows what are the possible actions, and it sees
a state/observation and performs an action and gets (possibly delayed) reward. Using this information, agent needs to improve actions over time. We call 'the actions taken by agent given a state' as policy.

Towards improving it's actions, agent may learn the value of a state (or state,action pair) that is indicative of cumulative reward (returns) obtained from starting in that state (or state,action pair). In some RL algorithms, agent does not learn this value function but directly learns the policy - those are called policy gradient methods.

So the Environment implementation should model how the state evolves and also the rewards that mimic the behavior of yield. And the agent should play with environment and we want to see if we can build an agent that can learn the 3-sisters model.

## Key design questions
For now, I am ignoring the external factors like weather, soil, water etc. With that, 

- There are two key aspects that we want our agents to learn : (1) effective spatial layout and (2) effective temporal structure that results in best yield. (The second aspect can be thought of as abstracting/simplifying the external factors like weather and water in addition to factors like when plants support each other) Our reward design should capture both these aspects while (loosely) matching the temporal / spatial relations between plants in effective 3-sisters planting model. 

> Open: Do we need to model 'harvesting' as a possible action for 'Environment'? Harvesting at the right time does not seem to be a complex decistion that agent needs to learn, we can alternately model 'automatic harvesting' within the environment i.e., as time progresses as a plant becomes ready to harvest, the environment automatically harvests the plant and makes the cells empty.

## Setup instructions
- You need to use pipenv with python3 (Read about it at https://pipenv-fork.readthedocs.io/en/latest/ and install it)
- After you clone the repository locally, do 'pipenv shell' on the root folder to initialize the virtual environment.
- If you are running for the first time, you probably need to do 'pipenv install' after the above (so that all packages are pulled in)
- From the root folder you need to do 'python -m pytest' to run all unit tests.
- Finally if you find anything wrong in the above instructions or if you know better ways, fix it and do a PR :-)
> We (atleast I) still need to figure out how to make the python imports work well such that you can run the above command from any sub-directory but currently running from a sub-directory gives importing failures.
## Implementation Notes
- Environment should follow gym interface for interplay with other code.
- A reference I used to approaximate reward design for 3-sisters: https://www.almanac.com/content/three-sisters-corn-bean-and-squash# , review the reward design below and let me know if you have any suggestions. Note that the below reward design is just some starting point and probably not a good one at all. It's overly simplistic for the actual 3-sisters crop system, but probably too specific for a reinforcement agent to learn. The intention is to find out how does an agent perform with such a reward design and improve it over time.
-  Code should be modular such that we should be able to add new rules to plant rewards OR new plants easily. One example additional rule I can thinkg of is to penalize corn/bean plants that are around the edges of field.
- Below details evolve over time:
  - Environment:
    - For simplicity, follow the current model of a fixed 'harvest' period for all plants, so 'harvest' period is part of environment, end of harvest period marks end of episode.
    - Fields: Size (n), Farm (n x n grid), each cell is an integer value of the plant. Reward at the end of episode is sum of rewards of cells. This is all same as what we already have. It's the plants that differ or implement some aspects of 3-sisters.
  - Plants:
    - Corn:
      - By default, after 'harvest' days produces yield of 1
      - If there is a surrounding plant Bean on day 4 - 6, the final yield is 1.1
      - If there was a surrounding plant Bean before day 4, the reward is going to be 0.8
      - If there is a surrounding Squash ever, it gets 0.7?
    -  Bean
        -  By the time, this is planted, if there is a Corn in neighborhood, it gets 1.1
        -  Only when the above is true, If Squash is planted in neighborhood after 6-8 days and Squah is the corner of grid, it gets 1.2 reward.
        -  Otherwise the reward is 1
    -  Squash
        -  When this is in corner of grid, the reward is 1.5
        -  Otherwise the reward is 0.7
-  Some ideas to manage the action space:
   -  The general environment takes in as action an entire specification of farm, this will be huge action space in general. One idea I have is to build wrapper environments that are sub-classes of this environment that restrict the action space the way they like. Accordingly, when an agent operating on these child classes sends it the restricted action space, the environment builds the complete action space that base class expects (based on it's rules). For example, one extension environment is take a 'plant type' as action, but plants in in natural sequence order of grid per each time step (and keeps track of current position to plant in internally). Another example is an environment that still takes only 'plant type' as action, initially plants it in the middle of field, and spreads the filed outward in a circular fashion. While I am not sure if this is helpful yet, this offers a modular way of defining different environments with restricted action spaces. See the code (version2/environment.py) for example ideas on how to build these.


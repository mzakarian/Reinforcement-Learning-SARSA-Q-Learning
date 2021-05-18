# Reinforcement Learning

Learn how to sail safely in dangerous waters to your goal by creating a generation based reinforcement learning model using Q-Learning or SARSA. 

## What makes the waters dangerous?

There are three types of tiles in the deterministic environment:
1. `no waves` - every action moves the boat by 0 additional fields
2. `yellow waves` - every action moves the boat by 1 additional field
3. `red waves` - every action moves the boat by 2 additional fields

> When you use the stochastic environment you can choose the probability of the waves.

## Configuration

You can configure:
- learning algorithm
- learning rate (alpha)
- discount factor (gamma)
- number of generations
- exploration and explotation proportion
- value of positive/negative rewards
- environment type (stochastic or deterministic)

## Statistics

The program automatically generates, shows and exports some related statistics. 

### Heatmaps
![heatmap](results/adv%2B_heatmap.png)

### Q-Values
A .csv file showing the q-value of every action (columns) for each episode (rows). 
![qvalues](results/adv%2B_qvalue.png)

### Rewards/Episode
![rewards](results/adv%2B_rewards.png)

### Steps/Episode
![steps](results/adv%2B_steps.png)

> This program was developed as part of a university project.

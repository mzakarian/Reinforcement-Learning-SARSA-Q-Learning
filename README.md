# Reinforcement Learning

Learn how to sail safely in dangerous waters to your goal by creating a generation based refinforcement learning model using Q-Learning or SARSA. 

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

## Stats

You can also generate some statistics, like:

### Heatmaps
![heatmap](results/adv%2B_heatmap.png)

### Q-Values
![heatmap](results/adv%2B_qvalue.png)

### Rewards/Episode
![heatmap](results/adv%2B_rewards.png)

### Steps/Episode
![heatmap](results/adv%2B_steps.png)

> This program was developed as part of a project at the university.

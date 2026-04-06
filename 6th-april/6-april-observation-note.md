# 6 April Task: User-Based Sharding - Observation Note

## Objective
Route messages by `user_id` and show shard imbalance when one user becomes highly active.

## Simulation Setup
- 3 shards
- Background traffic: 3,000 messages from random users
- Influencer spike: 5,000 messages from one user (`user_id = 9999`)
- Routing rule: `shard = user_id % number_of_shards`

## Actual Run Output
- Shard 0: 6031 messages (75.39% load)
- Shard 1: 982 messages (12.28% load)
- Shard 2: 987 messages (12.34% load)

## Observation
User-based sharding creates severe imbalance during influencer spikes. Because all influencer messages map to one shard, that shard is overloaded while other shards remain underutilized.

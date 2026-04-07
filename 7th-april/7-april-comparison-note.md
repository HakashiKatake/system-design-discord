# 7 April Task: Channel-Based Sharding - Comparison Note

## Objective
Route messages by channel_id and compare behavior with the previous user-based strategy.

## Routing Rule
- shard = channel_id % number_of_shards

## Actual Run Output (Day 7)
- Shard 0: 996 messages (12.45% load)
- Shard 1: 6003 messages (75.04% load)
- Shard 2: 1001 messages (12.51% load)

## Comparison With Day 6 (User-Based)
Day 6 output:
- Shard 0: 6031 messages (75.39% load)
- Shard 1: 982 messages (12.28% load)
- Shard 2: 987 messages (12.34% load)

Day 7 output:
- Shard 0: 996 messages (12.45% load)
- Shard 1: 6003 messages (75.04% load)
- Shard 2: 1001 messages (12.51% load)

## Observation
Both strategies create severe imbalance under spike conditions. The overloaded shard changes, but the hotspot problem remains:
- Day 6 hotspot came from one highly active user.
- Day 7 hotspot came from one viral channel.

This shows channel-based routing does not solve hotspot risk; it shifts hotspot ownership from user activity to channel popularity.

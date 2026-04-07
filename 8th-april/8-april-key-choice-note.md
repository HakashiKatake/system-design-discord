# 8 April Task: Hash-Based Sharding - Key Choice Note

## Objective
Implement hash-based routing and justify what key should be hashed.

## Key Choice
Chosen key: user_id:channel_id (composite)

Why this key was chosen:
- Hashing only user_id can still overload one shard when one user is extremely active.
- Hashing only channel_id can still overload one shard when one channel goes viral.
- Hashing a composite key spreads writes across more hash inputs and reduces both single-user and single-channel concentration.

## Routing Rule
- digest = md5(user_id:channel_id)
- shard = digest % number_of_shards

## Actual Run Output
- Shard 0: 2781 messages (34.76% load)
- Shard 1: 2558 messages (31.97% load)
- Shard 2: 2661 messages (33.26% load)

## Observation
Load is much more balanced compared with Day 6 and Day 7, where one shard carried about 75% of traffic. Hash-based routing with a composite key improves distribution under mixed spike patterns, though it may still require additional techniques when shard count changes.

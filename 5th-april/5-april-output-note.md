# 5 April Task: Shards Introduction - Output Note

## Objective
Create independent shards and store messages separately (no global message storage).

## Implementation
- Created `Shard` with its own `messages` list.
- Created `ShardManager` with 3 shards.
- Routed incoming messages using simple round-robin for baseline distribution.
- Simulated 5,000 messages.

## Actual Run Output
- Shard 0: 1667 messages
- Shard 1: 1667 messages
- Shard 2: 1666 messages

## Observation
The shard storage is independent and messages are physically separated by shard. This completes the Day 5 introduction requirement before testing intentionally bad routing strategies on later days.

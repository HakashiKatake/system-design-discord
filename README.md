# When Chat Systems Break - Realistic Sharding Simulation

This repository tracks day-by-day implementation of the Discord-like sharding assignment.

## Project Goal
Build a chat simulation from a naive single-server system toward sharded behavior, while observing:
- hotspots
- uneven load
- scaling trade-offs
- failure impact

## Assignment Timeline (2 April - 9 April)

| Date | Focus | Required Deliverable | Current Status | Evidence |
|---|---|---|---|---|
| 2 April | System Thinking | 1-page failure analysis (no coding) | Done | [2nd-april/2-april-system-thinking-analysis.md](2nd-april/2-april-system-thinking-analysis.md) |
| 3 April | Basic System | Working chat system + message count output | Done | [3rd-april/3-april-basic-chat-system.py](3rd-april/3-april-basic-chat-system.py) |
| 4 April | Scaling Awareness | Large-load simulation + short observation note | Done | [4th-april/4-april-scaling-awareness.py](4th-april/4-april-scaling-awareness.py), [4th-april/4-april-observation-note.md](4th-april/4-april-observation-note.md) |
| 5 April | Shards Introduction | Independent shards storing data separately | Done | [5th-april/5-april-shards-introduction.py](5th-april/5-april-shards-introduction.py), [5th-april/5-april-output-note.md](5th-april/5-april-output-note.md) |
| 6 April | User-Based Sharding | Route using user_id + shard distribution output | Done | [6th-april/6-april-user-based-sharding.py](6th-april/6-april-user-based-sharding.py), [6th-april/6-april-observation-note.md](6th-april/6-april-observation-note.md) |
| 7 April | Channel-Based Sharding | Route using channel_id + comparison note | Done | [7th-april/7-april-channel-based-sharding.py](7th-april/7-april-channel-based-sharding.py), [7th-april/7-april-comparison-note.md](7th-april/7-april-comparison-note.md) |
| 8 April | Hash-Based Sharding | Hash routing + key-choice explanation | Done | [8th-april/8-april-hash-based-sharding.py](8th-april/8-april-hash-based-sharding.py), [8th-april/8-april-key-choice-note.md](8th-april/8-april-key-choice-note.md) |
| 9 April | Stress + Failure Simulation | Logs + final code + analysis | Pending | Not started |

## Work Completed So Far

### Day 2 (2 April)
Completed system-failure analysis for spike traffic conditions:
- first bottlenecks and failure order
- hotspot behavior
- fast-growing data categories

### Day 3 (3 April)
Implemented a naive single-server chat system with:
- User, Channel, Message models
- ChatServer message storage
- message validation and message-count stats

Sample output:
- Users: 5
- Channels: 3
- Total messages: 10

### Day 4 (4 April)
Implemented single-server scaling simulation with measured results:
- Scenario A: 10 users, 1,000 messages
- Scenario B: 1,000 users, 100,000 messages
- runtime, throughput, and memory comparison

### Day 5 (5 April)
Implemented shard introduction with independent shard storage:
- 3 shards with per-shard `messages` list
- baseline routing with round-robin
- printed messages per shard

### Day 6 (6 April)
Implemented user-based sharding and simulated influencer spike:
- routing rule based on `user_id % num_shards`
- one influencer generated 5,000 messages
- clear imbalance observed in shard distribution

### Day 7 (7 April)
Implemented channel-based sharding and compared with Day 6:
- routing rule based on `channel_id % num_shards`
- one viral channel generated 5,000 messages
- hotspot remained (about 75% load on one shard), demonstrating channel popularity risk

### Day 8 (8 April)
Implemented hash-based sharding with explicit key-choice reasoning:
- selected composite key `user_id:channel_id`
- used MD5 hash modulo shard count for routing
- observed near-even load distribution under mixed spike traffic

## How to Run

From repository root:

```bash
source .venv/bin/activate
python 3rd-april/3-april-basic-chat-system.py
python 4th-april/4-april-scaling-awareness.py
python 5th-april/5-april-shards-introduction.py
python 6th-april/6-april-user-based-sharding.py
python 7th-april/7-april-channel-based-sharding.py
python 8th-april/8-april-hash-based-sharding.py
```

## Repository Structure

- [2nd-april/2-april-system-thinking-analysis.md](2nd-april/2-april-system-thinking-analysis.md)
- [3rd-april/3-april-basic-chat-system.py](3rd-april/3-april-basic-chat-system.py)
- [4th-april/4-april-scaling-awareness.py](4th-april/4-april-scaling-awareness.py)
- [4th-april/4-april-observation-note.md](4th-april/4-april-observation-note.md)
- [5th-april/5-april-shards-introduction.py](5th-april/5-april-shards-introduction.py)
- [5th-april/5-april-output-note.md](5th-april/5-april-output-note.md)
- [6th-april/6-april-user-based-sharding.py](6th-april/6-april-user-based-sharding.py)
- [6th-april/6-april-observation-note.md](6th-april/6-april-observation-note.md)
- [7th-april/7-april-channel-based-sharding.py](7th-april/7-april-channel-based-sharding.py)
- [7th-april/7-april-comparison-note.md](7th-april/7-april-comparison-note.md)
- [8th-april/8-april-hash-based-sharding.py](8th-april/8-april-hash-based-sharding.py)
- [8th-april/8-april-key-choice-note.md](8th-april/8-april-key-choice-note.md)
- [Assignment_ “When Chat Systems Break” - A Realistic Sharding Simulation.md](Assignment_%20%E2%80%9CWhen%20Chat%20Systems%20Break%E2%80%9D%20-%20A%20Realistic%20Sharding%20Simulation.md)
- [Assignment_ “When Chat Systems Break” - A Realistic Sharding Simulation.pdf](Assignment_%20%E2%80%9CWhen%20Chat%20Systems%20Break%E2%80%9D%20-%20A%20Realistic%20Sharding%20Simulation.pdf)

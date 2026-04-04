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
| 5 April | Shards Introduction | Independent shards storing data separately | Pending | Not started |
| 6 April | User-Based Sharding | Route using user_id + shard distribution output | Pending | Not started |
| 7 April | Channel-Based Sharding | Route using channel_id + comparison note | Pending | Not started |
| 8 April | Hash-Based Sharding | Hash routing + key-choice explanation | Pending | Not started |
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

## How to Run

From repository root:

```bash
source .venv/bin/activate
python 3rd-april/3-april-basic-chat-system.py
python 4th-april/4-april-scaling-awareness.py
```

## Repository Structure

- [2nd-april/2-april-system-thinking-analysis.md](2nd-april/2-april-system-thinking-analysis.md)
- [3rd-april/3-april-basic-chat-system.py](3rd-april/3-april-basic-chat-system.py)
- [4th-april/4-april-scaling-awareness.py](4th-april/4-april-scaling-awareness.py)
- [4th-april/4-april-observation-note.md](4th-april/4-april-observation-note.md)
- [Assignment_ “When Chat Systems Break” - A Realistic Sharding Simulation.md](Assignment_%20%E2%80%9CWhen%20Chat%20Systems%20Break%E2%80%9D%20-%20A%20Realistic%20Sharding%20Simulation.md)
- [Assignment_ “When Chat Systems Break” - A Realistic Sharding Simulation.pdf](Assignment_%20%E2%80%9CWhen%20Chat%20Systems%20Break%E2%80%9D%20-%20A%20Realistic%20Sharding%20Simulation.pdf)

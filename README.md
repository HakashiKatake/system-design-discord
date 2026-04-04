# When Chat Systems Break - Realistic Sharding Simulation

This repository tracks a day-by-day implementation of the assignment:
"When Chat Systems Break" (Discord-like system design and failure simulation).

## Project Goal
Build and evolve a chat platform simulation from a naive single-server model toward sharded architectures, while observing real-world failure modes:
- load hotspots
- uneven shard utilization
- scaling trade-offs
- failure impact and recovery limits

## Assignment Timeline (2 April - 9 April)

| Date | Focus | Required Deliverable | Current Status | Evidence |
|---|---|---|---|---|
| 2 April | System Thinking | 1-page failure analysis (no coding) | Done | [2-april-system-thinking-analysis.md](2-april-system-thinking-analysis.md) |
| 3 April | Basic System | Working chat system + message count output | Done | [3-april-basic-chat-system.py](3-april-basic-chat-system.py) <img width="478" height="77" alt="Screenshot 2026-04-03 at 6 12 30 PM" src="https://github.com/user-attachments/assets/3f386e57-db7f-4103-8477-063dee9a439d" />|
| 4 April | Scaling Awareness | Large-load simulation + short observation note | Pending | Not started |
| 3 April | Basic System | Working chat system + message count output | Done | [3-april-basic-chat-system.py](3-april-basic-chat-system.py) |
| 4 April | Scaling Awareness | Large-load simulation + short observation note | Done | [4-april-scaling-awareness.py](4-april-scaling-awareness.py), [4-april-observation-note.md](4-april-observation-note.md) |
| 5 April | Shards Introduction | Independent shards storing data separately | Pending | Not started |
| 6 April | User-Based Sharding | Route by user_id + uneven distribution output | Pending | Not started |
| 7 April | Channel-Based Sharding | Route by channel_id + comparison note | Pending | Not started |
| 8 April | Hash-Based Sharding | Hash-based routing + key-choice explanation | Pending | Not started |
| 9 April | Stress + Failure Simulation | Logs + final code + analysis | Pending | Not started |

## Work Completed So Far

### Day 2 (2 April)
Completed a system-failure analysis covering:
- first failure points under spike traffic
- bottlenecks (write path, memory, storage, hotspot channel)
- data growth patterns and likely failure sequence

### Day 3 (3 April)
Implemented a naive single-server chat system with:
- User, Channel, Message models
- ChatServer storage and validation
- send_message flow
- stats output including total messages

Sample output:
- Users: 5
- Channels: 3
- Total messages: 10

### Day 4 (4 April)
Implemented a single-server scaling simulation with measured load behavior:
- Small-load run (10 users, 1,000 messages)
- Large-load run (1,000 users, 100,000 messages)
- Runtime and memory comparison to show scaling stress

Artifacts:
- `4-april-scaling-awareness.py`
- `4-april-observation-note.md`

## How to Run (Day 3)

From repository root:

```bash
source .venv/bin/activate
python 3-april-basic-chat-system.py
```

## How to Run (Day 4)

From repository root:

```bash
source .venv/bin/activate
python 4-april-scaling-awareness.py
```

## Repository Structure

- `2-april-system-thinking-analysis.md` -> Day 2 written analysis
- `3-april-basic-chat-system.py` -> Day 3 working code
- `4-april-scaling-awareness.py` -> Day 4 load simulation code
- `4-april-observation-note.md` -> Day 4 short observation note
- `Assignment_ “When Chat Systems Break” - A Realistic Sharding Simulation.md` -> assignment brief (markdown)
- `Assignment_ “When Chat Systems Break” - A Realistic Sharding Simulation.pdf` -> assignment brief (original)

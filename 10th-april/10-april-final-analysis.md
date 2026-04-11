# 10 April: Final Analysis (Based on Day 9 Stress + Failure Simulation)

## Scope
This analysis is derived from running:
- `9th-april/9-april-stress-failure-simulation.py`

It covers all required final questions and mandatory features from the assignment brief.

## Final Comparison (3 shards)
- User-based: Stored 23054, Dropped 3946, Max shard load 39.42%, Query shards checked 3
- Channel-based: Stored 22928, Dropped 4072, Max shard load 45.22%, Query shards checked 3
- Hash-based: Stored 23024, Dropped 3976, Max shard load 39.65%, Query shards checked 3

## Answers to Required Questions

### 1) Which shard failed first and why?
In this simulation, **Shard 1 failed first** because it was intentionally disabled during Scenario 3 (extreme spike + failure) to model a real server outage.

Why this matters:
- Any write routed to the failed shard is dropped.
- This is visible in dropped write counts during Scenario 3:
  - User-based: 3946 dropped
  - Channel-based: 4072 dropped
  - Hash-based: 3976 dropped

Conclusion: once a shard is down, data loss appears immediately unless replication/failover exists.

### 2) Which strategy looked good but failed under spike?
**Channel-based sharding** looked simple and reasonable initially, but failed under viral-channel spike.

Evidence:
- During Scenario 2 (viral event), channel-based emitted hotspot warning:
  - `WARNING: hotspot detected (69.11% on busiest shard)`

Interpretation:
- Routing by `channel_id` sends all messages of a viral channel to one shard.
- This creates severe skew even when other shards are idle.

### 3) What happens if shards increase from 3 -> 10?
Observed from evolution summaries:

- User-based:
  - Max load drops from 39.64% (3 shards) -> 10.70% (10 shards)
  - Dropped writes reduce from 3965 -> 1222

- Hash-based:
  - Max load drops from 39.64% (3 shards) -> 10.76% (10 shards)
  - Dropped writes reduce from 4018 -> 1172

- Channel-based:
  - Still hotspot-prone at 10 shards (max load 38.24%)
  - Better than 3 shards but remains skewed because a viral channel is still a hotspot key

Additional trade-off:
- Query cost rises with shard count for cross-shard reads:
  - Shards checked: 3 -> 6 -> 10

### 4) What breaks when one shard goes down?
When one shard is down:
- Writes targeting that shard are lost (`Dropped writes` increases immediately)
- Data becomes incomplete/inconsistent across shards
- Read paths can miss expected messages if they were never stored due to dropped writes

System-level effect:
- Availability degrades for the key range routed to the failed shard
- Without retry-to-healthy-shard, replication, or failover, reliability is weak

## Mandatory Feature Coverage Check

### Cross-Shard Query
Implemented in `cross_shard_last_messages(channel_id, n=10)`:
- Gathers matching data from all shards
- Sorts by message ID descending
- Returns last 10 messages

### Hotspot Detection
Implemented with warning rule:
- If busiest shard has >50% of total load -> warning printed
- Verified with channel-based viral spike (69.11%)

### System Evolution
Implemented with comparative simulation at shard counts:
- 3, 6, and 10 shards
- Reports stored/dropped/max-load/query-scan cost per strategy

### Failure Simulation
Implemented by disabling one shard in Scenario 3:
- `set_shard_active(shard_id=1, active=False)`
- Captures impact as dropped writes and changed distribution

### Performance Awareness
Implemented by counting query scan breadth:
- `Shards checked for query` reported for each run
- Demonstrates read cost growth as shard count increases

## Final Conclusion
- User-based and channel-based strategies are easy to implement but fail under concentrated spike patterns.
- Hash-based with composite key (`user_id:channel_id`) gives better distribution, but does not eliminate failure risk when a shard is down.
- Increasing shards improves distribution and reduces dropped writes in this setup, but increases cross-shard query work.
- A production-ready design would need replication, failover, and more efficient query/indexing strategies beyond write routing.

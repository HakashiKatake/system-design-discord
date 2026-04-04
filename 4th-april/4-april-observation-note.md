# 4 April Task: Scaling Awareness - Observation Note

## What Was Simulated
Single-server chat system with in-memory message storage (`messages` list):
- Scenario A (small load): 10 users, 1,000 messages
- Scenario B (large load): 1,000 users, 100,000 messages (100x users and 100x messages)

## Measured Output

### Scenario A - Small load
- Elapsed: 0.0037 sec
- Throughput: 269,526.59 msg/sec
- Avg latency per message: 0.003710 ms
- Peak memory: 0.15 MB

### Scenario B - Large load
- Elapsed: 0.4192 sec
- Throughput: 238,540.02 msg/sec
- Avg latency per message: 0.004192 ms
- Peak memory: 17.14 MB

### Comparison
- Message volume increase: 100.0x
- Total runtime increase: 113.0x
- Peak memory increase: 113.8x

## Short Observation
The single-server design handles small load smoothly, but under 100x scale, total processing time and memory usage grow more than linearly in this run (~113x each). Even though average per-message latency only increases slightly, sustained growth in in-memory state shows why this model becomes inefficient and risky at larger scale (higher memory pressure, longer processing windows, and reduced headroom for traffic spikes).

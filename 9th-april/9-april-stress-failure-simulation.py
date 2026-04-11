from __future__ import annotations

from dataclasses import dataclass
import hashlib
import random
from typing import Callable


@dataclass
class Message:
    message_id: int
    user_id: int
    channel_id: int
    content: str


class Shard:
    def __init__(self, shard_id: int) -> None:
        self.id = shard_id
        self.active = True
        self.messages: list[Message] = []

    def store(self, message: Message) -> bool:
        if not self.active:
            return False
        self.messages.append(message)
        return True


class ShardManager:
    def __init__(self, num_shards: int, name: str) -> None:
        self.name = name
        self.shards = [Shard(i) for i in range(num_shards)]
        self.total_writes = 0
        self.failed_writes = 0

    def route_shard(self, message: Message) -> Shard:
        raise NotImplementedError

    def send_message(self, message: Message) -> None:
        shard = self.route_shard(message)
        self.total_writes += 1
        if not shard.store(message):
            self.failed_writes += 1

    def set_shard_active(self, shard_id: int, active: bool) -> None:
        self.shards[shard_id].active = active

    def messages_per_shard(self) -> list[int]:
        return [len(shard.messages) for shard in self.shards]

    def total_stored(self) -> int:
        return sum(self.messages_per_shard())

    def max_load_ratio(self) -> float:
        total = self.total_stored()
        if total == 0:
            return 0.0
        return max(self.messages_per_shard()) / total

    def hotspot_warning(self) -> str:
        ratio = self.max_load_ratio()
        if ratio > 0.5:
            return f"WARNING: hotspot detected ({ratio * 100:.2f}% on busiest shard)"
        return "OK: no hotspot above 50%"

    def print_distribution(self, label: str) -> None:
        counts = self.messages_per_shard()
        total = sum(counts)
        print(f"\n[{self.name}] {label}")
        for idx, count in enumerate(counts):
            pct = (count / total * 100) if total else 0.0
            state = "UP" if self.shards[idx].active else "DOWN"
            print(f"Shard {idx} ({state}): {count} messages ({pct:.2f}%)")
        print(f"Total writes attempted: {self.total_writes}")
        print(f"Stored messages: {self.total_stored()}")
        print(f"Dropped writes: {self.failed_writes}")
        print(self.hotspot_warning())

    def cross_shard_last_messages(self, channel_id: int, n: int = 10) -> tuple[list[Message], int]:
        # Performance awareness: track how many shards were checked for this query.
        checked = 0
        candidates: list[Message] = []

        for shard in self.shards:
            checked += 1
            for msg in shard.messages:
                if msg.channel_id == channel_id:
                    candidates.append(msg)

        candidates.sort(key=lambda m: m.message_id, reverse=True)
        return candidates[:n], checked


class UserShardManager(ShardManager):
    def route_shard(self, message: Message) -> Shard:
        return self.shards[message.user_id % len(self.shards)]


class ChannelShardManager(ShardManager):
    def route_shard(self, message: Message) -> Shard:
        return self.shards[message.channel_id % len(self.shards)]


class HashShardManager(ShardManager):
    def route_shard(self, message: Message) -> Shard:
        key = f"{message.user_id}:{message.channel_id}"
        digest = hashlib.md5(key.encode()).hexdigest()
        shard_id = int(digest, 16) % len(self.shards)
        return self.shards[shard_id]


def run_normal_day(manager: ShardManager, rng: random.Random, start_id: int) -> int:
    message_id = start_id
    for _ in range(5000):
        msg = Message(
            message_id=message_id,
            user_id=rng.randint(1, 1000),
            channel_id=rng.randint(1, 50),
            content="normal",
        )
        manager.send_message(msg)
        message_id += 1
    return message_id


def run_viral_event(manager: ShardManager, rng: random.Random, start_id: int) -> int:
    message_id = start_id

    for _ in range(2000):
        msg = Message(
            message_id=message_id,
            user_id=rng.randint(1, 1000),
            channel_id=rng.randint(1, 50),
            content="background",
        )
        manager.send_message(msg)
        message_id += 1

    viral_channel = 7
    for _ in range(8000):
        msg = Message(
            message_id=message_id,
            user_id=rng.randint(1, 20000),
            channel_id=viral_channel,
            content="viral",
        )
        manager.send_message(msg)
        message_id += 1

    return message_id


def run_extreme_spike_with_failure(manager: ShardManager, rng: random.Random, start_id: int) -> int:
    message_id = start_id

    # Disable one shard mid-test to simulate server failure.
    manager.set_shard_active(shard_id=1, active=False)

    for _ in range(12000):
        msg = Message(
            message_id=message_id,
            user_id=rng.randint(1, 30000),
            channel_id=rng.randint(1, 50),
            content="extreme",
        )
        manager.send_message(msg)
        message_id += 1

    return message_id


def evaluate_strategy(
    manager_factory: Callable[[int], ShardManager],
    shard_count: int,
    seed: int,
    verbose: bool = True,
) -> dict[str, float]:
    manager = manager_factory(shard_count)
    rng = random.Random(seed)
    next_id = 1

    next_id = run_normal_day(manager, rng, next_id)
    if verbose:
        manager.print_distribution("Scenario 1 - Normal day")

    next_id = run_viral_event(manager, rng, next_id)
    if verbose:
        manager.print_distribution("Scenario 2 - Viral event")

    next_id = run_extreme_spike_with_failure(manager, rng, next_id)
    if verbose:
        manager.print_distribution("Scenario 3 - Extreme spike + shard failure")

    # Mandatory feature: cross-shard query.
    last_msgs, shards_checked = manager.cross_shard_last_messages(channel_id=7, n=10)
    ids = [m.message_id for m in last_msgs]
    if verbose:
        print(f"Cross-shard query (channel=7): last 10 message IDs = {ids}")
        print(f"Shards checked for query: {shards_checked}")

    return {
        "stored": float(manager.total_stored()),
        "dropped": float(manager.failed_writes),
        "max_load_pct": manager.max_load_ratio() * 100.0,
        "query_shards_checked": float(shards_checked),
        "query_results": float(len(last_msgs)),
    }


def make_user_manager(shards: int) -> ShardManager:
    return UserShardManager(shards, "User-based")


def make_channel_manager(shards: int) -> ShardManager:
    return ChannelShardManager(shards, "Channel-based")


def make_hash_manager(shards: int) -> ShardManager:
    return HashShardManager(shards, "Hash-based(user:channel)")


def print_summary_table(title: str, rows: list[tuple[str, dict[str, float]]]) -> None:
    print(f"\n{title}")
    print("Strategy | Stored | Dropped | Max Shard Load % | Query Shards Checked | Query Results")
    print("-" * 90)
    for name, metrics in rows:
        print(
            f"{name} | {int(metrics['stored'])} | {int(metrics['dropped'])} | "
            f"{metrics['max_load_pct']:.2f}% | {int(metrics['query_shards_checked'])} | {int(metrics['query_results'])}"
        )


def run_evolution_analysis() -> None:
    print("\nSystem Evolution Check (3 -> 6 -> 10 shards) using same mixed workload")

    seed = 99
    shard_options = [3, 6, 10]

    for shard_count in shard_options:
        rows: list[tuple[str, dict[str, float]]] = []
        for label, factory in [
            ("User-based", make_user_manager),
            ("Channel-based", make_channel_manager),
            ("Hash-based", make_hash_manager),
        ]:
            rows.append((label, evaluate_strategy(factory, shard_count=shard_count, seed=seed, verbose=False)))

        print_summary_table(f"Evolution Summary - {shard_count} shards", rows)


def run_day9() -> None:
    print("Day 9: Stress + Failure Simulation")

    seed = 42
    rows: list[tuple[str, dict[str, float]]] = []

    for label, factory in [
        ("User-based", make_user_manager),
        ("Channel-based", make_channel_manager),
        ("Hash-based", make_hash_manager),
    ]:
        metrics = evaluate_strategy(factory, shard_count=3, seed=seed)
        rows.append((label, metrics))

    print_summary_table("Final Comparison - 3 shards", rows)

    # Mandatory feature: system evolution study.
    run_evolution_analysis()


if __name__ == "__main__":
    run_day9()

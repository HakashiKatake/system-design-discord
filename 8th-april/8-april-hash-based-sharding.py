from __future__ import annotations

from dataclasses import dataclass
import hashlib
import random


@dataclass
class Message:
    user_id: int
    channel_id: int
    content: str


class Shard:
    def __init__(self, shard_id: int) -> None:
        self.id = shard_id
        self.messages: list[Message] = []

    def store(self, message: Message) -> None:
        self.messages.append(message)


class ShardManager:
    def __init__(self, num_shards: int) -> None:
        self.shards = [Shard(i) for i in range(num_shards)]


class HashShardManager(ShardManager):
    def get_shard(self, key: str) -> Shard:
        digest = hashlib.md5(key.encode()).hexdigest()
        h = int(digest, 16)
        return self.shards[h % len(self.shards)]

    def make_key(self, message: Message) -> str:
        # Day 8 decision: hash a composite key to reduce single-user/single-channel hotspots.
        return f"{message.user_id}:{message.channel_id}"

    def send_message(self, message: Message) -> None:
        shard = self.get_shard(self.make_key(message))
        shard.store(message)

    def print_distribution(self) -> None:
        total = sum(len(shard.messages) for shard in self.shards)
        print("Messages per shard (hash routing with user_id:channel_id):")
        for shard in self.shards:
            count = len(shard.messages)
            load_pct = (count / total * 100) if total else 0.0
            print(f"Shard {shard.id}: {count} messages ({load_pct:.2f}% load)")


def simulate_mixed_spike(manager: HashShardManager) -> None:
    rng = random.Random(42)

    # Background traffic across users/channels.
    for i in range(3000):
        user_id = rng.randint(1, 1000)
        channel_id = rng.randint(1, 50)
        manager.send_message(Message(user_id=user_id, channel_id=channel_id, content=f"normal-{i}"))

    # Influencer spike (same user).
    influencer_id = 9999
    for i in range(2500):
        channel_id = rng.randint(1, 50)
        manager.send_message(Message(user_id=influencer_id, channel_id=channel_id, content=f"influencer-{i}"))

    # Viral channel spike (same channel).
    viral_channel_id = 7
    for i in range(2500):
        user_id = rng.randint(1, 1000)
        manager.send_message(Message(user_id=user_id, channel_id=viral_channel_id, content=f"viral-{i}"))


if __name__ == "__main__":
    shard_manager = HashShardManager(num_shards=3)
    simulate_mixed_spike(shard_manager)
    shard_manager.print_distribution()

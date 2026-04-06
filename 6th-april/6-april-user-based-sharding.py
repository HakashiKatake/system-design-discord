from __future__ import annotations

from dataclasses import dataclass
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


class UserShardManager(ShardManager):
    def get_shard(self, user_id: int) -> Shard:
        return self.shards[user_id % len(self.shards)]

    def send_message(self, message: Message) -> None:
        shard = self.get_shard(message.user_id)
        shard.store(message)

    def print_distribution(self) -> None:
        total = sum(len(shard.messages) for shard in self.shards)
        print("Messages per shard (user_id routing):")
        for shard in self.shards:
            count = len(shard.messages)
            load_pct = (count / total * 100) if total else 0.0
            print(f"Shard {shard.id}: {count} messages ({load_pct:.2f}% load)")


def simulate_user_spike(manager: UserShardManager) -> None:
    rng = random.Random(42)

    # Background traffic from many normal users.
    for i in range(3000):
        user_id = rng.randint(1, 1000)
        channel_id = rng.randint(1, 50)
        manager.send_message(Message(user_id=user_id, channel_id=channel_id, content=f"normal-{i}"))

    # One influencer sends massive traffic.
    influencer_id = 9999
    for i in range(5000):
        manager.send_message(Message(user_id=influencer_id, channel_id=7, content=f"influencer-{i}"))


if __name__ == "__main__":
    shard_manager = UserShardManager(num_shards=3)
    simulate_user_spike(shard_manager)
    shard_manager.print_distribution()

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
        self._next_index = 0

    def send_message(self, message: Message) -> None:
        # Day 5 goal: store data independently per shard.
        # We use simple round-robin routing as an initial distribution choice.
        shard = self.shards[self._next_index % len(self.shards)]
        shard.store(message)
        self._next_index += 1

    def print_distribution(self) -> None:
        print("Messages per shard:")
        for shard in self.shards:
            print(f"Shard {shard.id}: {len(shard.messages)} messages")


def simulate(manager: ShardManager, num_users: int = 1000, num_messages: int = 5000) -> None:
    rng = random.Random(42)

    for i in range(num_messages):
        user_id = rng.randint(1, num_users)
        channel_id = rng.randint(1, 50)
        message = Message(user_id=user_id, channel_id=channel_id, content=f"hello-{i}")
        manager.send_message(message)


if __name__ == "__main__":
    shard_manager = ShardManager(num_shards=3)
    simulate(shard_manager, num_users=1000, num_messages=5000)
    shard_manager.print_distribution()

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
import random
import tracemalloc


@dataclass
class Message:
    user_id: int
    channel_id: int
    content: str


class ChatServer:
    def __init__(self) -> None:
        self.messages: list[Message] = []

    def send_message(self, message: Message) -> None:
        self.messages.append(message)

    def stats(self) -> None:
        print(f"Total messages stored: {len(self.messages)}")


def run_simulation(num_users: int, num_messages: int, num_channels: int = 50) -> dict[str, float]:
    server = ChatServer()
    rng = random.Random(42)

    tracemalloc.start()
    start = perf_counter()

    for i in range(num_messages):
        user_id = rng.randint(1, num_users)
        channel_id = rng.randint(1, num_channels)
        msg = Message(user_id=user_id, channel_id=channel_id, content=f"hello-{i}")
        server.send_message(msg)

    elapsed = perf_counter() - start
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    server.stats()

    throughput = num_messages / elapsed if elapsed > 0 else 0.0
    avg_latency_ms = (elapsed / num_messages) * 1000 if num_messages > 0 else 0.0

    return {
        "num_users": float(num_users),
        "num_messages": float(num_messages),
        "elapsed_sec": elapsed,
        "throughput_msg_per_sec": throughput,
        "avg_latency_ms": avg_latency_ms,
        "current_mem_mb": current_mem / (1024 * 1024),
        "peak_mem_mb": peak_mem / (1024 * 1024),
    }


def print_result(title: str, result: dict[str, float]) -> None:
    print(f"\n{title}")
    print(f"Users: {int(result['num_users'])}")
    print(f"Messages: {int(result['num_messages'])}")
    print(f"Elapsed: {result['elapsed_sec']:.4f} sec")
    print(f"Throughput: {result['throughput_msg_per_sec']:.2f} msg/sec")
    print(f"Avg latency per message: {result['avg_latency_ms']:.6f} ms")
    print(f"Current memory: {result['current_mem_mb']:.2f} MB")
    print(f"Peak memory: {result['peak_mem_mb']:.2f} MB")


if __name__ == "__main__":
    print("Day 4: Scaling Awareness Simulation (Single Server)")

    small = run_simulation(num_users=10, num_messages=1_000)
    print_result("Scenario A - Small load (expected to work smoothly)", small)

    large = run_simulation(num_users=1_000, num_messages=100_000)
    print_result("Scenario B - Large load (100x users, single server)", large)

    print("\nComparison")
    print(f"Message volume increase: {large['num_messages'] / small['num_messages']:.1f}x")
    print(f"Total runtime increase: {large['elapsed_sec'] / small['elapsed_sec']:.1f}x")
    print(f"Peak memory increase: {large['peak_mem_mb'] / max(small['peak_mem_mb'], 1e-9):.1f}x")

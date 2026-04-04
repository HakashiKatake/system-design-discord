from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    user_id: int
    username: str


@dataclass
class Channel:
    channel_id: int
    name: str


@dataclass
class Message:
    user_id: int
    channel_id: int
    content: str
    created_at: datetime


class ChatServer:
    def __init__(self) -> None:
        self.users: dict[int, User] = {}
        self.channels: dict[int, Channel] = {}
        self.messages: list[Message] = []

    def add_user(self, user: User) -> None:
        self.users[user.user_id] = user

    def add_channel(self, channel: Channel) -> None:
        self.channels[channel.channel_id] = channel

    def send_message(self, message: Message) -> None:
        if message.user_id not in self.users:
            raise ValueError(f"Unknown user_id: {message.user_id}")
        if message.channel_id not in self.channels:
            raise ValueError(f"Unknown channel_id: {message.channel_id}")
        self.messages.append(message)

    def stats(self) -> None:
        print("Users:", len(self.users))
        print("Channels:", len(self.channels))
        print("Total messages:", len(self.messages))


if __name__ == "__main__":
    server = ChatServer()

    users = [
        User(1, "alice"),
        User(2, "bob"),
        User(3, "charlie"),
        User(4, "diana"),
        User(5, "eve"),
    ]

    channels = [
        Channel(101, "general"),
        Channel(102, "sports"),
        Channel(103, "tech"),
    ]

    for user in users:
        server.add_user(user)

    for channel in channels:
        server.add_channel(channel)

    demo_messages = [
        Message(1, 101, "Hi everyone", datetime.now()),
        Message(2, 101, "Hello Alice", datetime.now()),
        Message(3, 102, "Match starts in 10 mins", datetime.now()),
        Message(4, 103, "Anyone using Python 3.13?", datetime.now()),
        Message(5, 101, "Let us plan tonight's discussion", datetime.now()),
        Message(1, 102, "Who will win today?", datetime.now()),
        Message(2, 103, "I just upgraded my setup", datetime.now()),
        Message(3, 101, "Good to see everyone here", datetime.now()),
        Message(4, 102, "This channel is getting active", datetime.now()),
        Message(5, 103, "Sharing a quick tip soon", datetime.now()),
    ]

    for message in demo_messages:
        server.send_message(message)

    server.stats()

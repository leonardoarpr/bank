from dataclasses import dataclass


@dataclass
class EventDTO:
    type: str
    destination: str
    amount: int
    origin: str = None


@dataclass
class AccountDTO:
    account: str
    balance: int

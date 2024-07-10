from dataclasses import dataclass


@dataclass
class EventDTO:
    type: str
    amount: int
    destination: str = None
    origin: str = None


@dataclass
class AccountDTO:
    account: str
    balance: int

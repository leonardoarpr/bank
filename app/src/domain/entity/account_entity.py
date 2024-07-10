import json
import os
from dataclasses import asdict

from app.src.domain.dto.event_dto import EventDTO, AccountDTO
from app.src.domain.exception.event_exception import AccountNotFound, InsufficientFunds
from app.src.domain.interface.EventManagerInterface import EventManagerInterface
from app.src.infrastructure.config import Config

ident = 4


class EventManager(EventManagerInterface):
    def __init__(self):
        self.event_file = Config().ACCOUNT_PATH
        self.events = self.read_events()

    def read_events(self) -> tuple:
        if os.path.exists(self.event_file):
            with open(self.event_file, 'r') as file:
                return json.load(file)

    def get_balance(self, account_id: str) -> int:
        event = self.find_event(account_id)
        if event:
            return event['balance']
        raise AccountNotFound

    def reset_events(self) -> None:
        self.events = []
        self.write_events()

    def write_events(self) -> None:
        with open(self.event_file, 'w') as file:
            json.dump(self.events, file, indent=ident)

    def find_event(self, destination: str) -> any:
        return next((event for event in self.events if event['account'] == destination), None)

    def deposit(self, data: EventDTO) -> EventDTO:
        existing_record = self.find_event(data.destination)
        if existing_record:
            existing_record['balance'] += data.amount
            data.amount = existing_record['balance']
            self.write_events()
            return data
        self.events.append(asdict(AccountDTO(account=data.destination, balance=data.amount)))
        return data

    def withdraw(self, data: EventDTO) -> EventDTO:
        existing_record = self.find_event(data.origin)
        if existing_record:
            if existing_record['balance'] >= data.amount:
                existing_record['balance'] -= data.amount
                data.amount = existing_record['balance']
                self.write_events()
                return data
            raise InsufficientFunds(existing_record['balance'])
        raise AccountNotFound

    def transfer(self, data: EventDTO) -> (list, list):
        origin_record = self.find_event(data.origin)
        destination_record = self.find_event(data.destination)
        if destination_record is None:
            self.deposit(EventDTO(amount=0, destination=data.destination, type="deposit"))
            destination_record = self.find_event(data.destination)
        if origin_record:
            if origin_record['balance'] >= data.amount:
                origin_record['balance'] -= data.amount
                destination_record['balance'] += data.amount
                self.write_events()
                return origin_record, destination_record
            raise InsufficientFunds('Insufficient funds for origin', data.amount)
        raise AccountNotFound

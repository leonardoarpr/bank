import os
import unittest
from unittest.mock import patch, mock_open

from app.src.domain.dto.event_dto import EventDTO
from app.src.domain.entity.account_entity import EventManager
from app.src.domain.exception.event_exception import InsufficientFunds, AccountNotFound


class TestEventManager(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def setUp(self, mock_file):
        self.test_file = 'test_events.json'
        self.manager = EventManager(account_path=os.getenv('ACCOUNT_PATH'))

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('builtins.open', new_callable=mock_open)
    def test_deposit(self, mock_file):
        deposit_event = EventDTO(type="deposit", destination="100", amount=10)
        self.manager.deposit(deposit_event)
        self.assertEqual(len(self.manager.events), 1)
        self.assertEqual(self.manager.events[0]['balance'], 10)

    @patch('builtins.open', new_callable=mock_open)
    def test_deposit_into_created_account(self, mock_file):
        deposit_event_1 = EventDTO(type="deposit", destination="100", amount=10)
        deposit_event_2 = EventDTO(type="deposit", destination="100", amount=5)

        self.manager.deposit(deposit_event_1)
        self.manager.deposit(deposit_event_2)

        self.assertEqual(len(self.manager.events), 1)
        self.assertEqual(self.manager.events[0]['balance'], 15)

    @patch('builtins.open', new_callable=mock_open)
    def test_withdraw(self, mock_file):
        deposit_event = EventDTO(type="deposit", destination="100", amount=10)
        self.manager.deposit(deposit_event)

        withdraw_event = EventDTO(type="withdrawal", destination="100", amount=5)
        result = self.manager.withdraw(withdraw_event)
        self.assertEqual(result, withdraw_event)

    @patch('builtins.open', new_callable=mock_open)
    def test_withdraw_insufficient_funds(self, mock_file):
        deposit_event = EventDTO(type="deposit", destination="100", amount=10)
        self.manager.deposit(deposit_event)
        with self.assertRaises(InsufficientFunds):
            withdraw_event = EventDTO(type="withdraw", destination="100", amount=20)
            self.manager.withdraw(withdraw_event)

    @patch('builtins.open', new_callable=mock_open)
    def test_withdraw_account_not_found(self, mock_file):
        deposit_event = EventDTO(type="deposit", destination="100", amount=10)
        self.manager.deposit(deposit_event)
        with self.assertRaises(AccountNotFound):
            withdraw_event = EventDTO(type="withdraw", destination="200", amount=20)
            self.manager.withdraw(withdraw_event)

    @patch('builtins.open', new_callable=mock_open)
    def test_transfer(self, mock_file):
        deposit_event_1 = EventDTO(type="deposit", destination="100", amount=10)
        deposit_event_2 = EventDTO(type="deposit", destination="200", amount=5)

        self.manager.deposit(deposit_event_1)
        self.manager.deposit(deposit_event_2)
        deposit_event_2.origin = "100"

        self.manager.transfer(deposit_event_2)
        self.assertEqual(self.manager.events[0]['balance'], 5)
        self.assertEqual(self.manager.events[1]['balance'], 10)

    @patch('builtins.open', new_callable=mock_open)
    def test_transfer_insufficient_funds(self, mock_file):
        deposit_event_1 = EventDTO(type="deposit", destination="100", amount=5)
        deposit_event_2 = EventDTO(type="deposit", destination="200", amount=5)
        self.manager.deposit(deposit_event_1)
        self.manager.deposit(deposit_event_2)

        transfer_event = EventDTO(type="transfer", origin="100", destination="200", amount=10)
        with self.assertRaises(InsufficientFunds):
            self.manager.transfer(transfer_event)

    @patch('builtins.open', new_callable=mock_open)
    def test_transfer_account_not_found(self, mock_file):
        deposit_event_1 = EventDTO(type="deposit", destination="100", amount=5)
        deposit_event_2 = EventDTO(type="deposit", destination="200", amount=5)
        self.manager.deposit(deposit_event_1)
        self.manager.deposit(deposit_event_2)

        transfer_event = EventDTO(type="transfer", origin="100", destination="300", amount=10)
        with self.assertRaises(AccountNotFound):
            self.manager.transfer(transfer_event)

    @patch('builtins.open', new_callable=mock_open)
    def test_get_balance(self, mock_get_balance):
        deposit_event = EventDTO(type="deposit", destination="100", amount=10)
        self.manager.deposit(deposit_event)
        result = self.manager.get_balance(deposit_event.destination)
        print(result)
        self.assertEqual(result, deposit_event.amount)

    @patch('builtins.open', new_callable=mock_open)
    def test_empty_balance(self, mock_get_balance):
        deposit_event = EventDTO(type="deposit", destination="100", amount=10)
        # self.manager.deposit(deposit_event)
        with self.assertRaises(AccountNotFound):
            self.manager.get_balance(deposit_event.destination)

    @patch('builtins.open', new_callable=mock_open)
    def test_clear_events(self, mock_file):
        deposit_event = EventDTO(type="deposit", destination="100", amount=10)
        self.manager.deposit(deposit_event)
        self.manager.reset_events()
        self.assertListEqual(self.manager.events, [])


if __name__ == '__main__':
    unittest.main()

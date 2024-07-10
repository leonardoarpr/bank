import json

from cerberus import Validator

event_validator = {
    'type': {'type': 'string', 'required': True, 'allowed': ['deposit', 'withdraw', 'transfer']},
    'amount': {'type': 'integer', 'required': True, 'min': 1},
}

deposit_validator = {
    'type': {'type': 'string', 'required': True, 'allowed': ['deposit', 'withdraw', 'transfer']},
    'amount': {'type': 'integer', 'required': True, 'min': 1},
    'destination': {'type': 'string', 'required': True}
}

withdraw_validator = {
    'type': {'type': 'string', 'required': True, 'allowed': ['deposit', 'withdraw', 'transfer']},
    'amount': {'type': 'integer', 'required': True, 'min': 1},
    'origin': {'type': 'string', 'required': True}
}

transfer_validator = {
    'type': {'type': 'string', 'required': True, 'allowed': ['deposit', 'withdraw', 'transfer']},
    'amount': {'type': 'integer', 'required': True, 'min': 1},
    'destination': {'type': 'string', 'required': True},
    'origin': {'type': 'string', 'required': True}
}

event = Validator(event_validator, allow_unknown=True)
deposit = Validator(deposit_validator)
withdraw = Validator(withdraw_validator)
transfer = Validator(transfer_validator)


def event_validator(data):
    if not event.validate(data):
        raise ValueError(json.dumps(event.errors))


def deposit_validator(data):
    if not deposit.validate(data):
        raise ValueError(json.dumps(deposit.errors))


def withdraw_validator(data):
    if not withdraw.validate(data):
        raise ValueError(json.dumps(withdraw.errors))


def transfer_validator(data):
    if not transfer.validate(data):
        raise ValueError(json.dumps(transfer.errors))

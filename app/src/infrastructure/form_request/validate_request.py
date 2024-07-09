import json

from cerberus import Validator

event_validator = {
    'type': {'type': 'string', 'required': True, 'allowed': ['deposit', 'withdraw', 'transfer']},
    'destination': {'type': 'string', 'required': True},
    'amount': {'type': 'integer', 'required': True, 'min': 1},
    'origin': {'type': 'string', 'required': False}
}

event = Validator(event_validator)


def event_validator(data):
    if not event.validate(data):
        raise ValueError(json.dumps(event.errors))

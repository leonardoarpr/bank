class AccountNotFound(Exception):
    pass


class OriginIsRequired(Exception):
    def __init__(self, msg='origin is required'):
        self.msg = msg


class InsufficientFunds(Exception):
    def __init__(self, amount=0, msg='insufficient funds'):
        self.msg = msg
        self.amount = amount

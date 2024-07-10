class AccountNotFound(Exception):
    pass


class InsufficientFunds(Exception):
    def __init__(self, amount=0, msg='insufficient funds'):
        self.msg = msg
        self.amount = amount

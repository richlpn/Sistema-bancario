import logging
from dataclasses import dataclass
from enum import IntEnum

import bcrypt
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship

from Settings import HASH_SALT, ENCODING
from Utils.Exceptions import InvalidUser
from Utils.uuid_gen import generate_uuid
from .Trasactions import Transaction, Model, Base, TransactionTypes, InvalidTransaction, create_all

logger = logging.getLogger("UserModel")


class UserSettings(IntEnum):
    MIN_NAME_LENGTH = 25
    MAX_NAME_LENGTH = 5

    MIN_PASSWORD_LENGTH = 25
    MAX_PASSWORD_LENGTH = 5


@dataclass(eq=True, order=True)
class User(Model, Base):
    __tablename__ = "users"

    name = Column(String(25), nullable=False, unique=True)
    id = Column(String, primary_key=True, default=generate_uuid)
    password = Column(String, nullable=False)
    data_verified = False
    balance = Column(Float, default=0.0)

    transactions = relationship("Transaction", backref="users", lazy='subquery',
                                primaryjoin="and_(User.id==Transaction.sender_id)")

    def verify_password(self, password: str) -> bool:
        pwhash = bcrypt.hashpw(password.encode(ENCODING), HASH_SALT).decode(ENCODING)
        return self.password == pwhash

    def validate_user(self):
        if self.id is None:
            self.id = generate_uuid()
        if ("" != self.password is not None) and ("" != self.name is not None):
            self.__encrypt()
            self.data_verified = True
            return
        raise InvalidUser

    def __encrypt(self):
        self.password = bcrypt.hashpw(self.password.encode(ENCODING), HASH_SALT).decode(ENCODING)

    def __repr__(self):
        return f"<User name={self.name}, id={self.id}, password={self.password}>"

    def __str__(self):
        return f"<User name={self.name}, id={self.id}, password={self.password}>"

    def save(self, commit=True):

        if not self.data_verified:
            self.validate_user()
        super().save(commit=commit)

    def withdraw(self, value: float) -> Transaction:
        new_balance = self.balance - value
        if new_balance < 0 or value < 0: raise InvalidTransaction
        self.balance = new_balance
        t = Transaction(value=value, operation_type=TransactionTypes.WITHDRAW, sender_id=self.id, reciver_id=self.id)
        t.save()
        return t

    def deposit(self, value: float) -> Transaction:
        if value < 0: raise InvalidTransaction
        self.balance += value
        t = Transaction(value=value, operation_type=TransactionTypes.DEPOSIT,
                        sender_id=self.id, reciver_id=self.id)
        t.save()
        return t

    def transfer(self, value: float, user: "User") -> Transaction:

        new_balance = self.balance - value
        if new_balance < 0 or value < 0 or user is None or user.id == self.id:
            raise InvalidTransaction
        self.balance = new_balance
        user.balance += value

        t = Transaction(value=value, operation_type= TransactionTypes.TRANSFER, sender_id=self.id,reciver_id=user.id)
        return t

create_all()


def __main():
    # print("Main")
    adm: User = User.get_by_id("98ee2d00-a7d2-442d-a2bb-9dc02c8ca3dc")
    # t = Transaction(sender_id=adm.id, reciver_id=adm.id, value=1001, operation_type=1)
    # print(t)
    # t.save()
    print(adm.transactions[0].sender_id)


if __name__ == "__main__":
    __main()

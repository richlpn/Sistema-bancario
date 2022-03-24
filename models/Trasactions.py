from .model import Model, Base, create_all
from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from Utils.uuid_gen import generate_uuid
from Utils.Exceptions import InvalidTransaction
from enum import IntEnum

class TransactionTypes(IntEnum):

    DEPOSIT = 1
    WITHDRAW = 2
    TRANSFER = 3

class Transaction(Base,Model):
    __tablename__ = "transactions"


    id = Column(String, primary_key=True, default=generate_uuid)
    sender_id = Column(String, ForeignKey("users.id"))
    reciver_id = Column(String, ForeignKey("users.id"))
    value = Column(Float, default=0.0, nullable=False)
    operation_type = Column(Integer, nullable=False)

    # sender = relationship("User", back_populates="transactions",foreign_keys=[sender_id],)
    # # reciver = relationship("User", foreign_keys=[reciver_id],
    # #                        primaryjoin="and_(User.id==Transaction.reciver_id)")

    __valid_transaction = False
    def __repr__(self):
        return f"<Transaction value={self.value} operation_type={self.operation_type} >"

    def validate_transaction(self):
        valid_operation: bool = False

        for type in TransactionTypes:
            if self.operation_type == type:
                valid_operation = True

        if not self.sender_id and self.value and not valid_operation: raise InvalidTransaction
        self.__valid_transaction = True

    def save(self, commit=True):
        if not self.__valid_transaction:
            self.validate_transaction()
        super().save(commit=commit)

def bound():
    create_all()
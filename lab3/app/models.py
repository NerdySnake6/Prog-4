from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, nullable=False)
    name = Column(String, nullable=False)

    subscriptions = relationship("Subscription", back_populates="currency")

class Subscription(Base):
    __tablename__ = "subscriptions"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    currency_id = Column(Integer, ForeignKey("currencies.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="subscriptions")
    currency = relationship("Currency", back_populates="subscriptions")

    __table_args__ = (UniqueConstraint('user_id', 'currency_id', name='unique_subscription'),)

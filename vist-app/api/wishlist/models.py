from typing import List
from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from api.user.models import User
from datetime import datetime
from api.gift.models import Gift


wishlist_users_association = Table(
    'wishlist_users_association', 
    Model.metadata,
    Column('wishlist_id', ForeignKey('wishlists.id')),
    Column('user_id', ForeignKey('users.id'))         
)


class Wishlist(Model):
    __tablename__ = 'wishlists'

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    owner: Mapped[User] = relationship('User', back_populates='wishlists')
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    users: Mapped[List[User]] = relationship(secondary=wishlist_users_association)
    gifts: Mapped[List[Gift]] = relationship(back_populates="wishlist", cascade='all, delete-orphan')
    archived_at: Mapped[datetime] = mapped_column(nullable=True)

    @classmethod
    def get_all_columns(cls):
        return cls.__table__.columns.keys() + ['users', 'gifts']

    def __str__(self):
        return self.name
    
   
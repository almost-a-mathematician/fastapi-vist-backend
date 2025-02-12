from typing import List
from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from api.user.models import User
from datetime import datetime


wishlist_users_association = Table(
    'wishlist_users_association', 
    Model.metadata,
    Column('wishlist_id', ForeignKey('wishlists.id')),
    Column('user_id', ForeignKey('users.id'))         
)

class Wishlist(Model):
    __tablename__ = 'wishlists'

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    owner: Mapped[User] = relationship('User', cascade='all, delete')
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    users: Mapped[List['User']] = relationship(secondary=wishlist_users_association)
    archived_at: Mapped[datetime] = mapped_column(nullable=True)

    # добавить менеджер get_visible_for???
    
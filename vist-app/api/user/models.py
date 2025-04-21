from datetime import datetime
from typing import List
from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, DateTime, ForeignKey, String, Date, Table


user_friend_association = Table(
    'user_friend_association',
    Model.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('friend_id', ForeignKey('users.id'))
)

class User(Model):
    __tablename__ = 'users' 

    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    profile_pic: Mapped[str] = mapped_column(String(250), nullable=True) 
    birth_date: Mapped[Date] = mapped_column(Date, nullable=True)
    is_hidden_bd: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    friends: Mapped[List['User']] = relationship(
        secondary=user_friend_association, 
        cascade='all, delete',
        primaryjoin=('User.id == user_friend_association.c.user_id'),
        secondaryjoin=('User.id == user_friend_association.c.friend_id')
    )
    verified: Mapped[bool] = mapped_column(default=False) 
    
   




    
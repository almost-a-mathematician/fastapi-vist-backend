from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Float
from api.user.models import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.wishlist.models import Wishlist
class Gift(Model):
    __tablename__ = 'gifts'

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    img: Mapped[str | None] = mapped_column(String(250), nullable=True) 
    price: Mapped[float] = mapped_column(Float(10, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(String(150), nullable=True)
    link_url: Mapped[str] = mapped_column(String(200), nullable=False) 
    is_priority: Mapped[bool] = mapped_column(default=False, nullable=False)
    booked_by: Mapped[User | None] = relationship(cascade='all, delete')
    booked_by_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    wishlist_id: Mapped[int] = mapped_column(ForeignKey('wishlists.id'))
    wishlist: Mapped['Wishlist'] = relationship(back_populates="gifts", cascade='all, delete')
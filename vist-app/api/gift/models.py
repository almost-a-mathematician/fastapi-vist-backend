from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Float
from api.wishlist.models import Wishlist
from api.user.models import User


class Gift(Model):
    __tablename__ = 'gifts'

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    img: Mapped[str] = mapped_column(String(250), nullable=True) 
    price: Mapped[float] = mapped_column(Float(10, 2), nullable=False)
    description = Mapped[str] = mapped_column(String(150), nullable=True)
    link_url = Mapped[str] = mapped_column(String(200), nullable=False) 
    is_priority = Mapped[bool] = mapped_column(default=False, nullable=False)
    booked_by = Mapped[User | None] = relationship()
    booked_by_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), cascade='all, delete')
    wishlist_id: Mapped[int] = mapped_column(ForeignKey('wishlists.id'), cascade='all, delete')
    wishlist: Mapped[Wishlist] = relationship(back_populates="gifts")
    
   
   




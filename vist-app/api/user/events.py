from sqlalchemy import event
from api.user.models import User
from api.media.services.media import media_service
import asyncio


@event.listens_for(User, 'before_delete')
def delete_user_avatar(mapper, connection, model):
	if model.profile_pic:
		asyncio.create_task(media_service.delete(model.profile_pic))

from sqlalchemy import event
from api.gift.models import Gift
from api.media.services.media import media_service
import asyncio


@event.listens_for(Gift, 'before_delete')
def delete_gift_image(mapper, connection, model):
	if model.img:
		asyncio.create_task(media_service.delete(model.img))

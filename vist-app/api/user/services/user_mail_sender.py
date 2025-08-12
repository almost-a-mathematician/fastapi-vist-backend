from api.auth.services.mail_sender import mail_sender, MailSender
from api.user.models import User
import os
from datetime import datetime, timedelta
from api.user.services.db import user_service


class SendDelayException(BaseException):
    ...

class UserMailSender: 

    def __init__(self, mail_sender: MailSender, send_delay):
        self.mail_sender = mail_sender
        self.send_delay = send_delay
    
    async def create_and_send(self, user: User, template_filename, template_params):

        if user.last_email_at is not None and user.last_email_at + timedelta(minutes=self.send_delay) > datetime.now():
            raise SendDelayException
        
        await self.mail_sender.create_and_send(user.email, template_filename, template_params)
 
        await user_service.update(user.id, user, last_email_at=datetime.now())
   
user_mail_sender = UserMailSender(mail_sender, send_delay=int(os.getenv('USER_MAIL_SEND_DELAY')))
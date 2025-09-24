from pathlib import Path
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
import os


class MailSender:

	def __init__(self, smtp_username, smtp_password, email_from, smtp_port, smtp_host):
		conf = ConnectionConfig(
			MAIL_USERNAME=smtp_username,
			MAIL_PASSWORD=smtp_password,
			MAIL_FROM=email_from,
			MAIL_PORT=smtp_port,
			MAIL_SERVER=smtp_host,
			MAIL_STARTTLS=True,
			MAIL_SSL_TLS=False,
			TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates'
		)

		self.fm = FastMail(conf)

	async def create_and_send(self, email: str, template_filename, template_params):
		message = MessageSchema(subject='Vist', recipients=[email], template_body=template_params, subtype=MessageType.html, )

		await self.fm.send_message(message, template_name=template_filename)
		return True


mail_sender = MailSender(
	smtp_username=os.getenv('MAIL_USERNAME'),
	smtp_password=os.getenv('MAIL_PASSWORD'),
	email_from=os.getenv('MAIL_FROM'),
	smtp_port=int(os.getenv('MAIL_PORT')),
	smtp_host=os.getenv('MAIL_SERVER')
)

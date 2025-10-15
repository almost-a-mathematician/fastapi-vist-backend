from dotenv import load_dotenv

load_dotenv()  # получаем доступ к переменным .env

from fastapi import FastAPI
import uvicorn
from api.router import router as main_router
import admin
import os

app = FastAPI()
app.include_router(main_router)

if __name__ == '__main__':
	uvicorn.run(
		'main:app',
		host=os.getenv('HOST', default='127.0.0.1'),
		port=int(os.getenv('PORT', default=8085)),
		reload=True,
		forwarded_allow_ips='127.0.0.1',
		proxy_headers=True
	)

from dotenv import load_dotenv

load_dotenv() # получаем доступ к переменным .env


from fastapi import FastAPI
import uvicorn
from api.router import router as main_router

app = FastAPI()
app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8085, reload=True)
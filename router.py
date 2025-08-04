import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import User, UserInfo
from datetime import datetime, timedelta, date
from models import Users
import jwt
from environs import Env

# Загрузим секреты
env = Env()
env.read_env()

# Инициализируем логер
logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO')

# Инициализируем роутер
router = APIRouter(prefix="", tags=["salary"])

# Блок вспомогательных функций
def fill_table():
    """Функция использовалась для создания пробной базы"""
    test_users = [
        {
            "username": "Ivan",
            "password": "Ivan1",
            "salary": 275000.0,
            "salary_increase_date": date(2025, 11, 15)
        },
        {
            "username": "aaa",
            "password": "123",
            "salary": 175000.0,
            "salary_increase_date": date(2027, 11, 15)
        },
        {
            "username": "Kate",
            "password": "Kate1",
            "salary": 382000.0,
            "salary_increase_date": None
        },
    ]

    db = SessionLocal()
    if db.query(Users).count() != 0:
        logger.info('База уже есть')
        return None
    for user_data in test_users:
        user = Users(**user_data)
        db.add(user)
    db.commit()
    logger.info(f"Создана пробная база. Добавлено {len(test_users)} тестовых пользователя")

def check_password(user: User) -> bool:
    """Функция принимает login и password и проверяет есть ли такая пара в базе данных."""
    db = SessionLocal()
    users = db.execute(select(Users)).scalars().all()
    for some_user in users:
        if some_user.username == user.username and some_user.password == user.password:
            logger.info('Пароль принят')
            return True
    logger.info('Пароль отклонен')
    return False

def verify_token(token: str):
    try:
        payload = jwt.decode(token, key=env('SECRET_KEY'), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Блок эндпоинтов
@router.post("/login")
async def login(user: User):
    if check_password(user):
        payload = {
            "user_id": 1,
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, key=env('SECRET_KEY'), algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/salary_info", summary='Проверка ЗП')
async def get_salary_info(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        db: Session = Depends(get_db)
):
    payload = verify_token(token.credentials)
    user = db.execute(select(Users).where(Users.username == payload['username'])).scalars().first()
    message = (f"Привет, {user.username}! "
               f"Твоя текущая зарплата: {user.salary}. ")
    if user.salary_increase_date:
        message += f"Повышение будет {user.salary_increase_date}"
    else:
        message += f"А вот повышения тебе видимо не светит. Увы :((("
    return {'message': message}

import os
from dataclasses import dataclass

from dotenv import find_dotenv
from dotenv import load_dotenv


@dataclass
class AppData:
    admin_login: str
    admin_password: str


@dataclass
class MainPathData:
    admin_path: str


@dataclass
class Config:
    app: AppData
    main_path: MainPathData


def load_config() -> Config:
    if not find_dotenv():
        exit('Переменные окружения не загружены т.к отсутствует файл .env')
    else:
        load_dotenv()
    config = Config(
        app=AppData(
            admin_login=os.getenv('ADMIN_LOGIN'),
            admin_password=os.getenv('ADMIN_PASSWORD'),
        ),
        main_path=MainPathData(
            admin_path=os.getenv('ADMIN_URL')
        )
    )
    return config

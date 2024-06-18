import os

from dotenv import load_dotenv
# from pydantic.v1 import BaseSettings

# from API.services.slides.utils import LocalSlideManager, S3SlideManager

load_dotenv()
__POSTGRES_USER = os.getenv("POSTGRES_USER")
__POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
__POSTGRES_DB = os.getenv("POSTGRES_DB")
__POSTGRES_NETWORK_SOCKET = os.getenv("POSTGRES_NETWORK_SOCKET")
DB_DSN: str = f"postgresql+asyncpg://{__POSTGRES_USER}:{__POSTGRES_PASSWORD}@{__POSTGRES_NETWORK_SOCKET}/{__POSTGRES_DB}"

__REDIS_NETWORK_SOCKET = os.getenv("REDIS_NETWORK_SOCKET")
REDIS_DSN: str = f"redis://{__REDIS_NETWORK_SOCKET}"

SLIDE_PATH: str = r"files/"

##### этот блок почему то не работает . . странно
# class Settings(BaseSettings):
#     POSTGRES_USER: str #= "postgres"
#     POSTGRES_PASSWORD: str #= "postgres"
#     POSTGRES_DB: str #= "SVSViewer"
#     POSTGRES_NETWORK_SOCKET: str #= "localhost:5432"
#     DB_DSN: str = f"postgresql+asyncpg://{__POSTGRES_USER}:{__POSTGRES_PASSWORD}@{__POSTGRES_NETWORK_SOCKET}/{__POSTGRES_DB}"
#
#     REDIS_NETWORK_SOCKET = "localhost:6379"
#     REDIS_DSN: str = f"redis://{__REDIS_NETWORK_SOCKET}"
#
#     SLIDE_PATH: str = r"files/"
#
#
#     class Config:
#         env_file = "../.env"


# settings = Settings()

if os.name == 'nt':
    openslide_path = os.getcwd() + r'\openslide-bin-4.0.0.3-windows-x64\bin'
    os.environ['PATH'] = openslide_path + ";" + os.environ['PATH']

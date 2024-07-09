import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_DEBUG = os.getenv('APP_DEBUG')
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    PYTHON_PATH = os.getenv('PYTHON_PATH')
    ACCOUNT_PATH = os.getenv('ACCOUNT_PATH')

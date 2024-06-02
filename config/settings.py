from pydantic import BaseSettings
import os

'''
def get_app_env():
    app_env = os.getenv('APP_ENV','dev') 

    if app_env == 'prod':
        return '.env.prod'
    else:
        return '.env'
'''

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = '.env'
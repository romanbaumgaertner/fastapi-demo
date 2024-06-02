
from dotenv import dotenv_values
import os

def get_app_env():
    app_env = os.getenv('APP_ENV','dev') 

    if app_env == 'dev':
        print("Development")
        return '.env'
    else:
        print("Production")
        return '.env.prod'
    
def get_config():

    env = get_app_env()
    config = dotenv_values( env ) 
    print( config )

    return config
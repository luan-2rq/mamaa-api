from os import getenv

config = {
    'host': getenv('APP_HOST'),
    'port': getenv('APP_PORT'),
    'redis': {
        'name': getenv('REDIS_DATABASE_NAME'),
        'password': getenv('REDIS_PASSWORD'),
        'host': getenv('REDIS_HOST'),
        'port': getenv('REDIS_PORT'),  
    }
}
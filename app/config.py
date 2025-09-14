import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    """Base config."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    TESTING = False
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
class ProductionConfig(Config):
    """Production config."""
    ENV = 'production'
    
class DevelopmentConfig(Config):
    """Development config."""
    ENV = 'development'
    DEBUG = True
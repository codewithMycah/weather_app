from flask import Flask, render_template
from .config import DevelopmentConfig, ProductionConfig

import logging

import os
from dotenv import load_dotenv
load_dotenv()

# Logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s - %(filename)s:%(lineno)d: %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

def create_app():
    
    app = Flask(__name__)
    
    if os.getenv('FLASK_ENV') == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)
        
    logger.info('Flask application created and configured')
    
    @app.route('/')
    def main():
        return render_template('home.html')
    
    @app.route('/error')
    def error():
        return render_template('api_error.html')
    
    return app

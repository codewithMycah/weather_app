from flask import Flask, render_template, request, jsonify
from .config import DevelopmentConfig, ProductionConfig
import httpx
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
    
    # Open Meteo API
    app.api = None
    try:
        from .openmeteoapi import OpenMeteo
        app.api = OpenMeteo()
        
        logger.info("[OpenMeteo API] Imported successfully")
    except ImportError as ie:
        logger.warning(f"[OpenMeteo API] Module Import Error: {str(ie)}")
        app.api = None
    except Exception as e:
        logger.error(f"[OpenMeteo API] Error has occured: {str(e)}")
        app.api = None
    
    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            city_name = request.form.get('city_name').lower()
            logger.info(f"City Name: {city_name}")
            
        return render_template('home.html')
    
    @app.route('/search')
    def search():
        query = request.args.get("q", "").lower()
        logger.info(f"City Name: {query}")
            
        try:
            response = httpx.get(f"{os.getenv('API_URL_GEOCODING')}/search?name={query}&count=5&language=en&format=json")
            response.raise_for_status()  # raise exception for 4xx/5xx
            
            if response:
                results = response.json()  # parse JSON response
        except httpx.RequestError as e:
            results = {"error": f"Request error: {e}"}
        except httpx.HTTPStatusError as e:
            results = {"error": f"HTTP error: {e.response.status_code}"}
        return jsonify(results)
    
    @app.route('/error')
    def error():
        return render_template('error/api_error.html')
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404
    
    return app

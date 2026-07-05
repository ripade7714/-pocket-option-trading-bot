"""
Weather Dashboard - Main Application
Fetches and displays weather data from OpenWeatherMap API
"""
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_BASE = 'https://api.openweathermap.org/data/2.5'
FORECAST_API_BASE = 'https://api.openweathermap.org/data/2.5/forecast'

if not WEATHER_API_KEY:
    logger.warning("WEATHER_API_KEY not found in environment variables")

class WeatherService:
    """Service for fetching weather data"""
    
    @staticmethod
    def get_current_weather(city, units='metric'):
        """
        Get current weather for a city
        
        Args:
            city (str): City name
            units (str): Units for temperature (metric, imperial)
            
        Returns:
            dict: Weather data or None if error
        """
        try:
            url = f"{WEATHER_API_BASE}/weather"
            params = {
                'q': city,
                'appid': WEATHER_API_KEY,
                'units': units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched weather for {city}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather for {city}: {e}")
            return None
    
    @staticmethod
    def get_forecast(city, units='metric', count=40):
        """
        Get weather forecast for a city (5 days, 3-hour interval)
        
        Args:
            city (str): City name
            units (str): Units for temperature
            count (int): Number of forecast entries
            
        Returns:
            dict: Forecast data or None if error
        """
        try:
            url = f"{FORECAST_API_BASE}"
            params = {
                'q': city,
                'appid': WEATHER_API_KEY,
                'units': units,
                'cnt': count
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched forecast for {city}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching forecast for {city}: {e}")
            return None
    
    @staticmethod
    def get_weather_by_coordinates(lat, lon, units='metric'):
        """
        Get weather by latitude and longitude
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            units (str): Units for temperature
            
        Returns:
            dict: Weather data or None if error
        """
        try:
            url = f"{WEATHER_API_BASE}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': WEATHER_API_KEY,
                'units': units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched weather for coordinates ({lat}, {lon})")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather for coordinates: {e}")
            return None
    
    @staticmethod
    def get_multiple_cities_weather(cities, units='metric'):
        """
        Get weather for multiple cities
        
        Args:
            cities (list): List of city names
            units (str): Units for temperature
            
        Returns:
            dict: Weather data for all cities
        """
        weather_data = {}
        for city in cities:
            data = WeatherService.get_current_weather(city, units)
            if data:
                weather_data[city] = data
        return weather_data


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    """API endpoint for current weather"""
    try:
        city = request.args.get('city', 'London')
        units = request.args.get('units', 'metric')
        
        if not city:
            return jsonify({'error': 'City parameter is required'}), 400
        
        data = WeatherService.get_current_weather(city, units)
        
        if data is None:
            return jsonify({'error': 'Failed to fetch weather data'}), 500
        
        if 'cod' in data and data['cod'] == '404':
            return jsonify({'error': 'City not found'}), 404
        
        # Format response
        weather_info = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'wind_speed': data['wind']['speed'],
            'clouds': data['clouds']['all'],
            'timestamp': datetime.fromtimestamp(data['dt']).isoformat(),
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat(),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat(),
            'visibility': data.get('visibility', 'N/A')
        }
        
        return jsonify(weather_info), 200
    except Exception as e:
        logger.error(f"Error in get_current_weather: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather/forecast', methods=['GET'])
def get_forecast():
    """API endpoint for weather forecast"""
    try:
        city = request.args.get('city', 'London')
        units = request.args.get('units', 'metric')
        
        if not city:
            return jsonify({'error': 'City parameter is required'}), 400
        
        data = WeatherService.get_forecast(city, units)
        
        if data is None:
            return jsonify({'error': 'Failed to fetch forecast data'}), 500
        
        if 'cod' in data and data['cod'] != '200':
            return jsonify({'error': 'City not found'}), 404
        
        # Format forecast data
        forecast_list = []
        for item in data['list']:
            forecast_item = {
                'timestamp': datetime.fromtimestamp(item['dt']).isoformat(),
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
                'wind_speed': item['wind']['speed'],
                'clouds': item['clouds']['all'],
                'rain_probability': item.get('pop', 0) * 100
            }
            forecast_list.append(forecast_item)
        
        forecast_info = {
            'city': data['city']['name'],
            'country': data['city']['country'],
            'forecast': forecast_list
        }
        
        return jsonify(forecast_info), 200
    except Exception as e:
        logger.error(f"Error in get_forecast: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather/coordinates', methods=['GET'])
def get_weather_coordinates():
    """API endpoint for weather by coordinates"""
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        units = request.args.get('units', 'metric')
        
        if not lat or not lon:
            return jsonify({'error': 'Latitude and longitude parameters are required'}), 400
        
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return jsonify({'error': 'Invalid latitude or longitude'}), 400
        
        data = WeatherService.get_weather_by_coordinates(lat, lon, units)
        
        if data is None:
            return jsonify({'error': 'Failed to fetch weather data'}), 500
        
        # Format response
        weather_info = {
            'city': data['name'],
            'country': data['sys']['country'],
            'coordinates': {'lat': data['coord']['lat'], 'lon': data['coord']['lon']},
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'wind_speed': data['wind']['speed'],
            'clouds': data['clouds']['all'],
            'timestamp': datetime.fromtimestamp(data['dt']).isoformat()
        }
        
        return jsonify(weather_info), 200
    except Exception as e:
        logger.error(f"Error in get_weather_coordinates: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather/multiple', methods=['POST'])
def get_multiple_weather():
    """API endpoint for multiple cities weather"""
    try:
        data = request.get_json()
        
        if not data or 'cities' not in data:
            return jsonify({'error': 'cities parameter is required'}), 400
        
        cities = data.get('cities', [])
        units = data.get('units', 'metric')
        
        if not isinstance(cities, list) or len(cities) == 0:
            return jsonify({'error': 'cities must be a non-empty list'}), 400
        
        weather_data = WeatherService.get_multiple_cities_weather(cities, units)
        
        if not weather_data:
            return jsonify({'error': 'Failed to fetch weather data for any city'}), 500
        
        # Format response
        formatted_data = {}
        for city, raw_data in weather_data.items():
            formatted_data[city] = {
                'city': raw_data['name'],
                'country': raw_data['sys']['country'],
                'temperature': raw_data['main']['temp'],
                'feels_like': raw_data['main']['feels_like'],
                'humidity': raw_data['main']['humidity'],
                'description': raw_data['weather'][0]['description'],
                'icon': raw_data['weather'][0]['icon'],
                'wind_speed': raw_data['wind']['speed']
            }
        
        return jsonify(formatted_data), 200
    except Exception as e:
        logger.error(f"Error in get_multiple_weather: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_configured': bool(WEATHER_API_KEY)
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    if not WEATHER_API_KEY:
        print("ERROR: WEATHER_API_KEY not set. Please add it to .env file")
        print("Get your API key from: https://openweathermap.org/api")
        exit(1)
    
    logger.info("Starting Weather Dashboard...")
    app.run(debug=True, host='0.0.0.0', port=5000)

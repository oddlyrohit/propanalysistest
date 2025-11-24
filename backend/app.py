from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from services.data_aggregator import DataAggregatorService
from config import config
from middleware import register_error_handlers, register_request_tracker
from api.suburbs import suburbs_bp, init_routes

load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', static_url_path='')

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:5001').split(','),
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize data aggregator service
data_service = DataAggregatorService()

# Register middleware
register_error_handlers(app)
register_request_tracker(app)

# Initialize and register blueprints
init_routes(data_service)
app.register_blueprint(suburbs_bp, url_prefix='/api')


# SPA route handler - serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve static files or index.html for SPA routing"""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # Check if static folder has index.html
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return jsonify({
                "message": "Flask API is running",
                "note": "Frontend not built yet. Run 'npm run build' in frontend directory."
            })

if __name__ == '__main__':
    logger.info(f"Starting Flask application - Port: {config.FLASK_PORT}, Debug: {config.FLASK_DEBUG}")
    logger.info(f"Microburbs API Base URL: {config.MICROBURBS_API_BASE_URL}")
    logger.info(f"Using mock data mode: {config.USE_MOCK_DATA}")
    app.run(host='0.0.0.0', port=config.FLASK_PORT, debug=config.FLASK_DEBUG)


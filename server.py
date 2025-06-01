from flask import Flask, send_from_directory, abort, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get files directory from environment variable
FILES_DIR = os.getenv('FILES_DIR', 'files')

# Constants
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 * 1024  # 5GB
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route('/<filename>')
def serve_file(filename):
    """Serve a file from the files directory."""
    try:
        # Secure the filename to prevent directory traversal
        secure_name = secure_filename(filename)
        if secure_name != filename:
            abort(400, "Invalid filename")
            
        return send_from_directory(FILES_DIR, secure_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)
    except Exception as e:
        app.logger.error(f"Error serving file {filename}: {str(e)}")
        abort(500)

@app.route('/')
def index():
    """Simple index page."""
    return "File sharing server is running. Access files via /filename"

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size limit exceeded."""
    return "File too large", 413

if __name__ == '__main__':
    # Ensure files directory exists
    os.makedirs(FILES_DIR, exist_ok=True)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080) 
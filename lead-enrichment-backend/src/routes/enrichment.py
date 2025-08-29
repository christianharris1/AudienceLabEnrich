from flask import Blueprint, request, jsonify
import requests
import os

enrichment_bp = Blueprint('enrichment', __name__)

# API configuration - use environment variables for security
API_BASE_URL = os.environ.get('API_ENDPOINT', 'https://v3-api-job-72802495918.us-east1.run.app')
API_KEY = os.environ.get('API_KEY', 'sk_x1lvKiIZzXvRuZPyBi4QQaazSIvsXVCmmnXS3Bci5g')

@enrichment_bp.route('/enrich', methods=['POST'])
def enrich_lead():
    """
    Proxy endpoint for lead enrichment API
    """
    try:
        # Get the request data from the frontend
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Prepare the API request
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': API_KEY
        }
        
        # Make the request to the enrichment API
        response = requests.post(
            f'{API_BASE_URL}/enrich',
            json=request_data,
            headers=headers,
            timeout=30
        )
        
        # Return the response from the API
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                'error': f'API Error: {response.status_code}',
                'message': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 408
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection error'}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@enrichment_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({'status': 'healthy', 'service': 'lead-enrichment-proxy'}), 200


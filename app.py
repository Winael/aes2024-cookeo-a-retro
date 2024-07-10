import os
import logging
from flask import Flask, render_template, jsonify, request
from mocks.mock_firestore import MockFirestore

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

# Log the FLASK_ENV value
flask_env = os.environ.get('FLASK_ENV', 'Not set')
logging.info(f"FLASK_ENV: {flask_env}")

# Initialize the database connection (outside the function)
if os.environ.get('FLASK_ENV') == 'development':
   db = MockFirestore()
   logging.info("Using MockFirestore in development mode")  # Log that MockFirestore is being used

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/level.html')
def level():
    try:
        correlation_id = request.args.get('correlationID')
        logging.info(f"Level route called with correlationID: {correlation_id}")
        return render_template('level.html', correlation_id=correlation_id)
    except Exception as e:
        logging.error(f"Error in level route: {e}")  # Log the error
        return jsonify({'error': str(e)}), 500
    
@app.route('/create_retrospective', methods=['POST'])
def create_retrospective():
    try:
        data = request.get_json()
        correlation_id = data.get('correlationID')

        if not correlation_id:
            logging.error("Missing correlationID in request")  # Log an error if correlationID is missing
            return jsonify({'error': 'Missing correlationID'}), 400

        logging.info(f"Adding retrospective with correlationID: {correlation_id}")  # Log the correlationID
        db.collection('retrospectives').add({'correlationID': correlation_id})
        return jsonify({'message': 'Retrospective created successfully'})
    except Exception as e:
        logging.error(f"Error creating retrospective: {e}")  # Log the error
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')

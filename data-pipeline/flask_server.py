# data-pipeline/app.py
from flask import Flask, jsonify
import subprocess
import threading
import os

PORT = os.getenv('PORT')
app = Flask(__name__)

# Path to the data extraction script
DATA_EXTRACTION_SCRIPT = "/app/index.py"

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200

@app.route('/start', methods=['GET'])
def trigger_extraction():
    try:
        # Run the data extraction script in a separate thread to prevent blocking
        thread = threading.Thread(target=run_extraction)
        thread.start()
        return jsonify({"message": "Data extraction started."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_extraction():
    try:
        # Execute the data extraction script
        subprocess.run(["python", DATA_EXTRACTION_SCRIPT], check=True)
    except subprocess.CalledProcessError as e:
        # Log the error if the script fails
        print(f"Data extraction failed: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
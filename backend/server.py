import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

# Add root folder to sys.path so we can import 'monitor' package without Phase 1-3 modifications
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from monitor import logs_reader
    from monitor import detector
except ImportError as e:
    print(f"Failed to import monitor module safely. Error: {e}")
    sys.exit(1)

app = Flask(__name__)
# Enable CORS for all routes so our React dashboard can ingest metrics
CORS(app)

@app.route('/logs', methods=['GET'])
def get_logs():
    """Returns the raw logs chronologically fetched directly from attack_log.json."""
    try:
        logs = logs_reader.read_logs()
        return jsonify(logs), 200
    except Exception as e:
        # Failsafe fallback ensuring Valid JSON object always returned
        return jsonify([]), 500

@app.route('/analysis', methods=['GET'])
def get_analysis():
    """Channels logs into detector.py engine and serves deterministic threat results."""
    try:
        logs = logs_reader.read_logs()
        analysis = detector.analyze_logs(logs)
        return jsonify(analysis), 200
    except Exception as e:
        # Failsafe dictionary mapping requested frontend fields
        return jsonify({
            "total_files": 0,
            "time_taken": 0.0,
            "alert_level": "LOW",
            "risk_score": 0,
            "summary": "System offline or log read error.",
            "attack_detected": False
        }), 500

PORT = 3600

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)

import os
import json

# Absolute path resolution assuming `monitor/logs_reader.py` relative to `data/attack_log.json`
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
LOG_FILE = os.path.join(PROJECT_ROOT, "trojan", "data", "attack_log.json")

def read_logs():
    """
    Reads the attack logs line-by-line.
    Returns a list of parsed JSON objects (dictionaries).
    Handles missing the file and JSON corruption gracefully.
    """
    logs = []
    
    # Check if log file exists
    if not os.path.exists(LOG_FILE):
        return logs

    try:
        with open(LOG_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    # Attempt to parse individually to prevent single corrupt line failing all
                    entry = json.loads(line)
                    logs.append(entry)
                except json.JSONDecodeError:
                    pass # Ignore malformed logs
    except Exception as e:
        # Failsafe in case of file lock or permissions issues
        print(f"[ERROR] Exception reading log file: {e}")
        
    return logs

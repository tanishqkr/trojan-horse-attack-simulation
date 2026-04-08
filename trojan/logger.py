import os
import json
from datetime import datetime

# Configure data directory and log file relative to this script
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
LOG_FILE = os.path.join(DATA_DIR, "attack_log.json")

def _ensure_data_dir():
    """Ensures the data directory exists."""
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
        except Exception as e:
            print(f"[LOGGER ERROR] Failed to create data directory: {e}")

def log_event(event_type, file_path=None, status="SUCCESS", **kwargs):
    """
    Logs an event in structured JSON line format.
    Appends events line-by-line avoiding full file re-write.
    """
    _ensure_data_dir()
    
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "file": file_path,
            "status": status
        }
        
        # Include bonus fields like 'duration' or 'total_files'
        if kwargs:
            log_entry.update(kwargs)
            
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
            
    except Exception as e:
        # Fallback to prevent crash as per requirements
        print(f"[LOGGER ERROR] Exception writing to log file: {str(e)}")

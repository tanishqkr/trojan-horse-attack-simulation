import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEV_PATH = os.path.join(BASE_DIR, "trojan", "data", "attack_log.json")
PROD_PATH = os.path.expanduser("~/Desktop/cybersec_data/attack_log.json")

def _write_to_path(path, data_str):
    """Helper to write to a specific path, creating directories if needed."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as f:
            f.write(data_str + "\n")
    except Exception as e:
        print(f"[LOGGER ERROR] Failed to write to {path}: {e}")

def log_event(event_type, file_path=None, status="SUCCESS", **kwargs):
    """
    Logs an event in structured JSON line format.
    Appends events line-by-line avoiding full file re-write.
    """
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
            
        data_str = json.dumps(log_entry)
        
        _write_to_path(DEV_PATH, data_str)
        _write_to_path(PROD_PATH, data_str)
            
    except Exception as e:
        # Fallback to prevent crash as per requirements
        print(f"[LOGGER ERROR] Exception creating log entry: {str(e)}")

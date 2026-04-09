import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEV_PATH = os.path.join(BASE_DIR, "trojan", "data", "attack_log.json")
PROD_PATH = os.path.expanduser("~/Desktop/cybersec_data/attack_log.json")

def _read_from_path(path):
    logs = []
    print(f"[DEBUG] Attempting to read logs from: {path}")
    if not os.path.exists(path):
        print(f"[DEBUG] Path does not exist: {path}")
        return logs

    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    logs.append(entry)
                except json.JSONDecodeError:
                    pass
        print(f"[DEBUG] Successfully read {len(logs)} logs from {path}")
    except Exception as e:
        print(f"[ERROR] Exception reading log file {path}: {e}")
        
    return logs

def read_logs():
    """
    Reads the attack logs line-by-line from both DEV and PROD paths.
    Returns a deduplicated, parsed list of JSON objects (dictionaries) sorted by timestamp.
    """
    all_logs = []
    all_logs.extend(_read_from_path(DEV_PATH))
    all_logs.extend(_read_from_path(PROD_PATH))

    # Deduplicate entries based on timestamp + file + event
    unique_logs = {}
    for entry in all_logs:
        # Gracefully handle missing keys
        ts = entry.get("timestamp", "")
        evt = entry.get("event", "")
        fpath = entry.get("file", "")
        key = f"{ts}|{evt}|{fpath}"
        unique_logs[key] = entry
        
    deduplicated = list(unique_logs.values())
    
    # Sort logs chronologically by timestamp
    deduplicated.sort(key=lambda x: x.get("timestamp", ""))
    
    return deduplicated

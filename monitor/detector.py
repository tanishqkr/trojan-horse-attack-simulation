import sys
import os
from datetime import datetime

# Path setup tracking to root project folder so we can use package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from monitor import logs_reader

def analyze_logs(logs):
    """
    Analyzes log entries for specific Trojan behaviors.
    Returns a dictionary of analysis metrics and classifications.
    """
    if not logs:
        return {
            "total_files": 0,
            "time_taken": 0.0,
            "alert_level": "LOW",
            "risk_score": 0,
            "summary": "No logs found. System is quiet.",
            "attack_detected": False
        }
    
    encrypt_timestamps = []
    error_count = 0

    for entry in logs:
        # Gracefully handle missing dictionary fields
        event = entry.get("event")
        status = entry.get("status")
        timestamp_str = entry.get("timestamp")
        
        if not event or not timestamp_str:
            continue
            
        if status == "ERROR":
            error_count += 1
            
        if event == "FILE_ENCRYPTED" and status == "SUCCESS":
            try:
                # Parse ISO-8601 format timestamp
                dtime = datetime.fromisoformat(timestamp_str)
                encrypt_timestamps.append(dtime)
            except ValueError:
                continue

    # Sort chronological encryption timestamps
    encrypt_timestamps.sort()
    total_files = len(encrypt_timestamps)
    
    if total_files == 0:
        return {
            "total_files": 0,
            "time_taken": 0.0,
            "alert_level": "LOW",
            "risk_score": 0,
            "summary": "No successful file encryptions observed.",
            "attack_detected": False
        }
        
    time_taken = (encrypt_timestamps[-1] - encrypt_timestamps[0]).total_seconds()
    
    # Calculate Rapid Encryption (Max Files in any 5-second sliding window)
    # NOTE: This uses O(n^2). For massive log scales, a two-pointer sliding window (O(n)) is optimal.
    max_in_5s = 0
    for start_time in encrypt_timestamps:
        # Count all timestamps within 5 seconds of the start_time
        count = sum(1 for dt in encrypt_timestamps if 0 <= (dt - start_time).total_seconds() <= 5)
        if count > max_in_5s:
            max_in_5s = count

    # Determine alert level and base risk score
    alert_level = "LOW"
    risk_score = min((total_files * 3) + (max_in_5s * 5) + (error_count * 2), 100)
    summary = "Normal behavior detected. No major threats."

    # Business Rules implementation
    if total_files > 15:
        # BULK ENCRYPTION DETECTED
        alert_level = "HIGH"
        summary = f"CRITICAL: Bulk Encryption Detected. {total_files} files encrypted."
        risk_score = max(risk_score, 85)
    elif max_in_5s > 5:
        # RAPID ENCRYPTION DETECTED
        alert_level = "MEDIUM"
        summary = f"WARNING: Rapid Encryption Detected. {max_in_5s} files encrypted in <=5 seconds."
        risk_score = max(risk_score, 60)
    elif total_files > 0:
        # NORMAL / LOW BEHAVIOR
        summary = f"Minor file encryption activity observed ({total_files} files)."
        risk_score = max(risk_score, 10)

    # Spike in errors modifier
    if error_count > 5 and alert_level == "LOW":
        summary = f"Suspicious system errors ({error_count}) combined with file activity."
        risk_score = min(risk_score + 15, 100)

    # Cap risk score just in case
    risk_score = min(round(risk_score), 100)
    attack_detected = True if alert_level != "LOW" else False

    return {
        "total_files": total_files,
        "time_taken": round(time_taken, 2),
        "alert_level": alert_level,
        "risk_score": risk_score,
        "summary": summary,
        "attack_detected": attack_detected
    }

if __name__ == "__main__":
    logs = logs_reader.read_logs()
    analysis = analyze_logs(logs)

    # Requested CLI Test Output
    print(f"Total files encrypted: {analysis['total_files']}")
    print(f"Time taken: {analysis['time_taken']} seconds")
    print(f"ALERT LEVEL: {analysis['alert_level']}")
    
    # Bonus additions
    print(f"Risk Score: {analysis['risk_score']}%")
    print(f"Summary: {analysis['summary']}")
    print(f"Attack Detected: {analysis['attack_detected']}")

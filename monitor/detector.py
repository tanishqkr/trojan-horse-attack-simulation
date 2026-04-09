import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from monitor import logs_reader

def analyze_logs(logs):
    """
    Analyzes log entries for specific Trojan behaviors with improved accuracy.
    Handles unique file tracking, burst-based duration, and non-cumulative timeline.
    """
    res = {
        "total_files": 0,
        "unique_files": 0,
        "total_events": 0,
        "attack_duration": 0.0,
        "timeline": [],
        "alert_level": "LOW",
        "risk_score": 0,
        "summary": "No logs found. System is quiet.",
        "attack_detected": False,
        "time_taken": 0.0
    }
    
    if not logs:
        return res

    encrypt_timestamps = []
    unique_paths = set()
    total_events = 0
    error_count = 0
    timeline_dict = {}

    for entry in logs:
        event = entry.get("event")
        status = entry.get("status")
        timestamp_str = entry.get("timestamp")
        file_path = entry.get("file")
        
        if not event or not timestamp_str:
            continue
            
        if status == "ERROR":
            error_count += 1
            
        if event == "FILE_ENCRYPTED" and status == "SUCCESS":
            total_events += 1
            if file_path:
                unique_paths.add(file_path)
            
            try:
                dtime = datetime.fromisoformat(timestamp_str)
                encrypt_timestamps.append(dtime)
                
                time_key = dtime.replace(microsecond=0)
                timeline_dict[time_key] = timeline_dict.get(time_key, 0) + 1
            except ValueError:
                continue

    encrypt_timestamps.sort()
    unique_files_count = len(unique_paths)
    
    if total_events == 0:
        res.update({
            "unique_files": unique_files_count,
            "total_events": total_events,
            "summary": "System monitoring active. No threats detected." if error_count < 5 else "System errors observed, but no attack detected."
        })
        return res

    last_session = []
    if encrypt_timestamps:
        last_session = [encrypt_timestamps[0]]
        for i in range(1, len(encrypt_timestamps)):
            gap = (encrypt_timestamps[i] - encrypt_timestamps[i-1]).total_seconds()
            if gap > 10:
                last_session = [encrypt_timestamps[i]]
            else:
                last_session.append(encrypt_timestamps[i])
    
    attack_duration = 0.0
    if last_session:
        attack_duration = (last_session[-1] - last_session[0]).total_seconds()

    timeline_items = []
    for dt, count in timeline_dict.items():
        timeline_items.append({
            "dt": dt,
            "time": dt.strftime("%H:%M:%S"),
            "count": count
        })
    
    timeline_items.sort(key=lambda x: x["dt"])
    timeline = [{"time": item["time"], "count": item["count"]} for item in timeline_items]

    max_in_5s = 0
    for start_time in encrypt_timestamps:
        count = sum(1 for dt in encrypt_timestamps if 0 <= (dt - start_time).total_seconds() <= 5)
        if count > max_in_5s:
            max_in_5s = count

    calculated_risk = (unique_files_count * 5) + (max_in_5s * 6) + (error_count * 2)
    risk_score = min(calculated_risk, 100)

    alert_level = "LOW"
    summary = f"Minor file activity observed ({unique_files_count} unique files)."
    
    if risk_score >= 80 or unique_files_count > 15:
        alert_level = "HIGH"
        summary = f"CRITICAL: Massive file encryption detected! {unique_files_count} files affected."
    elif risk_score >= 40 or max_in_5s > 6:
        alert_level = "MEDIUM"
        summary = f"WARNING: Suspicious encryption burst. {max_in_5s} events per 5s detected."

    attack_detected = True if alert_level != "LOW" or risk_score > 30 else False

    return {
        "total_files": unique_files_count,
        "unique_files": unique_files_count,
        "total_events": total_events,
        "attack_duration": round(attack_duration, 2),
        "timeline": timeline,
        "alert_level": alert_level,
        "risk_score": round(risk_score),
        "summary": summary,
        "attack_detected": attack_detected,
        "time_taken": round((encrypt_timestamps[-1] - encrypt_timestamps[0]).total_seconds(), 2)
    }

if __name__ == "__main__":
    logs = logs_reader.read_logs()
    analysis = analyze_logs(logs)

    print(f"Unique Files: {analysis['unique_files']}")
    print(f"Total Events: {analysis['total_events']}")
    print(f"Burst Duration: {analysis['attack_duration']} seconds")
    print(f"Risk Score: {analysis['risk_score']}%")
    print(f"Alert Level: {analysis['alert_level']}")

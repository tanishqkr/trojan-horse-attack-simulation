import os
import base64
import hashlib
from datetime import datetime

# Core configuration
BASE_FOLDER = os.path.expanduser("~/Desktop")
TARGET_FOLDER_NAME = "demo1"
LOCKED_FOLDER_NAME = "demo1_locked"

# Derived paths
TARGET_FOLDER_PATH = os.path.join(BASE_FOLDER, TARGET_FOLDER_NAME)
LOCKED_FOLDER_PATH = os.path.join(BASE_FOLDER, LOCKED_FOLDER_NAME)
KEY_FILE_PATH = os.path.expanduser("~/Desktop/key.txt")

def generate_key():
    """
    Generates a secure key suitable for Fernet encryption.
    Uses basic random bytes and SHA-256 for determinism with random seeds.
    """
    try:
        random_bytes = os.urandom(32)
        key = base64.urlsafe_b64encode(hashlib.sha256(random_bytes).digest())
        return key
    except Exception as e:
        print(f"[UTILS] Failed to generate key: {e}")
        return None

def save_key(key):
    """
    Saves the generated string key to the key file with a timestamp.
    """
    try:
        with open(KEY_FILE_PATH, "a") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{timestamp} :: {key.decode()}\n")
    except Exception as e:
        print(f"[UTILS] Failed to save key: {e}")

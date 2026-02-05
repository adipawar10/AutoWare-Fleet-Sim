import boto3
import json
import datetime
import threading
import os

# Initialize S3 Client
s3 = boto3.client('s3', region_name='us-east-1')

# REPLACE THIS WITH YOUR ACTUAL BUCKET NAME
BUCKET_NAME = "adi-autoware-logs-2026"

def log_telemetry(robot_list):
    """
    Uploads robot status to AWS S3 in a non-blocking background thread.
    """
    # 1. Prepare data (runs on main thread)
    timestamp = datetime.datetime.now().isoformat()
    data = {
        "timestamp": timestamp,
        "robots": [
            {
                "id": r.id,
                "battery": r.battery,
                "position": r.pos,
                "state": r.state 
            } for r in robot_list
        ]
    }
    file_name = f"logs/telemetry_{timestamp}.json"

    # 2. Define the background task
    def upload_worker():
        try:
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=file_name,
                Body=json.dumps(data),
                ContentType='application/json'
            )
            print(f"✅ [AWS] Background Upload Success: {file_name}")
        except Exception as e:
            print(f"⚠️ [AWS] Upload Failed: {str(e)}")

    # 3. Fire and Forget (Start the thread)
    thread = threading.Thread(target=upload_worker)
    thread.start()
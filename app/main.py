import os
import threading
import time
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.monitor import check_json_endpoint, check_xml_endpoint

app = FastAPI(title="Cloud-Native Health Monitor")

TARGET_JSON = os.getenv("TARGET_JSON_URL", "https://httpbin.org/json")
TARGET_XML = os.getenv("TARGET_XML_URL", "https://httpbin.org/xml")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS", "15"))

def monitor_loop():
    while True:
        check_json_endpoint(TARGET_JSON, expected_key="slideshow")
        check_xml_endpoint(TARGET_XML, expected_tag="slideshow")
        time.sleep(POLL_INTERVAL)

@app.on_event("startup")
def start_poller():
    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()

@app.get("/healthz")
def liveness():
    return {"status": "healthy"}

@app.get("/ready")
def readiness():
    return {"status": "ready"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
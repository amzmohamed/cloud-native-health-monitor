import time
import requests
import defusedxml.ElementTree as ET
from prometheus_client import Counter, Gauge

ENDPOINT_UP = Gauge("endpoint_up", "Status of target endpoint (1 = UP, 0 = DOWN)", ["target"])
ENDPOINT_LATENCY = Gauge("endpoint_latency_seconds", "HTTP request latency in seconds", ["target"])
CHECK_FAILURES = Counter("endpoint_validation_failures_total", "Count of failed payload validations", ["target", "reason"])

def check_json_endpoint(url: str, expected_key: str, timeout: float = 3.0) -> bool:
    start_time = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        latency = time.time() - start_time
        ENDPOINT_LATENCY.labels(target=url).set(latency)

        if response.status_code != 200:
            ENDPOINT_UP.labels(target=url).set(0)
            CHECK_FAILURES.labels(target=url, reason="http_error").inc()
            return False

        data = response.json()
        if expected_key not in data:
            ENDPOINT_UP.labels(target=url).set(0)
            CHECK_FAILURES.labels(target=url, reason="schema_mismatch").inc()
            return False

        ENDPOINT_UP.labels(target=url).set(1)
        return True
    except Exception:
        ENDPOINT_LATENCY.labels(target=url).set(time.time() - start_time)
        ENDPOINT_UP.labels(target=url).set(0)
        CHECK_FAILURES.labels(target=url, reason="unreachable").inc()
        return False

def check_xml_endpoint(url: str, expected_tag: str, timeout: float = 3.0) -> bool:
    start_time = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        latency = time.time() - start_time
        ENDPOINT_LATENCY.labels(target=url).set(latency)

        if response.status_code != 200:
            ENDPOINT_UP.labels(target=url).set(0)
            CHECK_FAILURES.labels(target=url, reason="http_error").inc()
            return False

        root = ET.fromstring(response.content)
        if root.find(f".//{expected_tag}") is None and root.tag != expected_tag:
            ENDPOINT_UP.labels(target=url).set(0)
            CHECK_FAILURES.labels(target=url, reason="xml_tag_missing").inc()
            return False

        ENDPOINT_UP.labels(target=url).set(1)
        return True
    except Exception:
        ENDPOINT_LATENCY.labels(target=url).set(time.time() - start_time)
        ENDPOINT_UP.labels(target=url).set(0)
        CHECK_FAILURES.labels(target=url, reason="unreachable").inc()
        return False
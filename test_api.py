import subprocess
import time
import requests
import sys
from pathlib import Path


BASE_URL = "http://127.0.0.1:8000"


def start_server():
    """Start the FastAPI server using uvicorn in a subprocess for tests."""
    project_root = Path(__file__).parent
    # Use python -m uvicorn so that it works in most environments
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app"],
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Wait for server to start
    time.sleep(2)
    return proc


def stop_server(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


class TestAPI:
    @classmethod
    def setup_class(cls):
        cls.server_proc = start_server()

    @classmethod
    def teardown_class(cls):
        stop_server(cls.server_proc)

    def test_status_endpoint(self):
        resp = requests.get(f"{BASE_URL}/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data == {"status": "ok"}

    def test_sum_endpoint_valid(self):
        resp = requests.get(f"{BASE_URL}/sum", params={"a": 2, "b": 3})
        assert resp.status_code == 200
        data = resp.json()
        assert data["sum"] == 5

    def test_sum_endpoint_float(self):
        resp = requests.get(f"{BASE_URL}/sum", params={"a": 1.5, "b": 2.5})
        assert resp.status_code == 200
        data = resp.json()
        assert data["sum"] == 4.0

    def test_sum_missing_param(self):
        resp = requests.get(f"{BASE_URL}/sum", params={"a": 1})
        # FastAPI will return 422 for validation error (missing required parameter)
        assert resp.status_code == 422

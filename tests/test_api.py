import subprocess
import sys
import time
import requests

BASE = "http://127.0.0.1:5000"

_server_proc = None

def setup_module(module):
    """Start the Flask app in a subprocess before tests run."""
    global _server_proc
    # Start app.py using the same Python interpreter
    _server_proc = subprocess.Popen([sys.executable, "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for server to be ready
    for _ in range(20):
        try:
            r = requests.get(f"{BASE}/status", timeout=1)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(0.5)

    # If server didn't start, capture logs and fail
    out, err = _server_proc.communicate(timeout=1)
    raise RuntimeError(f"Flask server failed to start. stdout:\n{out}\nstderr:\n{err}")


def teardown_module(module):
    """Stop the Flask app after tests finish."""
    global _server_proc
    if _server_proc:
        _server_proc.terminate()
        try:
            _server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _server_proc.kill()


def test_status_ok():
    r = requests.get(f"{BASE}/status", timeout=5)
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_sum_ok():
    r = requests.get(f"{BASE}/sum?a=2&b=3", timeout=5)
    assert r.status_code == 200
    assert r.json() == {"sum": 5.0}


def test_sum_float_and_negative():
    r = requests.get(f"{BASE}/sum?a=2.5&b=-1.2", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert "sum" in data
    assert abs(data["sum"] - 1.3) < 1e-9


def test_sum_bad_params():
    r = requests.get(f"{BASE}/sum?a=foo&b=3", timeout=5)
    assert r.status_code == 400
    data = r.json()
    assert "error" in data

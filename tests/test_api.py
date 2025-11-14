import requests

BASE = "http://127.0.0.1:5000"

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

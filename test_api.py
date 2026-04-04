import requests

url = "https://campusgrid-api.onrender.com/nodes/register"
print(f"Testing POST to {url}...")
try:
    # Missing auth and body, but should NOT return 404 if the path exists
    resp = requests.post(url, timeout=10)
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text}")
except Exception as e:
    print(f"Error: {e}")

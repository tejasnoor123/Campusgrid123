import os
import redis
import ssl
from dotenv import load_dotenv

# Load agent's .env
env_path = os.path.join("agent", ".env")
load_dotenv(dotenv_path=env_path)

REDIS_URL = os.getenv("REDIS_URL")

print(f"Testing Redis connection to: {REDIS_URL[:20]}...{REDIS_URL[-20:]}")

try:
    kwargs = {"decode_responses": True}
    if REDIS_URL.startswith("rediss://"):
        kwargs["ssl_cert_reqs"] = ssl.CERT_NONE
    
    r = redis.from_url(REDIS_URL, **kwargs)
    print("Pinging Redis...")
    response = r.ping()
    print(f"Success! PONG: {response}")
except Exception as e:
    print(f"Failed to connect: {e}")

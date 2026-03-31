import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"
    DNS_RESOLVER = os.getenv("DNS_RESOLVER", None)  # Optional: Custom DNS resolver
    REQUIRE_DNSSEC = os.getenv("REQUIRE_DNSSEC", "True") == "True"

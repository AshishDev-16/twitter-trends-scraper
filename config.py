import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI')

# ProxyMesh Configuration
PROXYMESH_USERNAME = os.getenv('PROXYMESH_USERNAME')
PROXYMESH_PASSWORD = os.getenv('PROXYMESH_PASSWORD')
PROXYMESH_ENDPOINTS = [
    "proxy.proxymesh.com:31280",  # Main endpoint
    "us.proxymesh.com:31280",     # US endpoint
    "open.proxymesh.com:31280"    # Open endpoint
]

# Twitter Configuration
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD') 
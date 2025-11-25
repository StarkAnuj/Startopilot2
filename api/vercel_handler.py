"""
Vercel serverless function handler for FastAPI
"""
import os
import sys

# Add the parent directory to the path so we can import from api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

# For Vercel deployment
handler = app
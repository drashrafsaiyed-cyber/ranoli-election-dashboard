"""Vercel serverless function entry point."""
import sys
from pathlib import Path

# Add project root to path so imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app

# Vercel expects the WSGI app to be named 'app'

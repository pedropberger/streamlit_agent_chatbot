#!/usr/bin/env python3
import os
import subprocess
import sys

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import requests
        print("✅ All dependencies are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install the required dependencies using: pip install -r requirements.txt")
        return False

def run_app():
    """Run the Streamlit app"""
    try:
        print("Starting Streamlit app...")
        subprocess.run(["streamlit", "run", "app.py"])
        return True
    except Exception as e:
        print(f"❌ Error running Streamlit app: {e}")
        return False

if __name__ == "__main__":
    print("Checking dependencies...")
    if check_dependencies():
        run_app()
    else:
        sys.exit(1)
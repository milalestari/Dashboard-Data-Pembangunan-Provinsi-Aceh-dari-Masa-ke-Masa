#!/usr/bin/env python3
"""
Quick launcher script for Aceh Development Dashboard
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required files exist"""
    required_files = [
        "main_app.py",
        "requirements.txt",
        "config.py",
        "utils.py",
        "data_processor.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing required files: {missing_files}")
        return False
    return True

def run_dashboard():
    """Run the Streamlit dashboard"""
    print("Starting Aceh Development Dashboard...")
    print("Dashboard will open in your browser at: http://localhost:8501")
    print("Press Ctrl+C to stop the dashboard")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main_app.py"])
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    except Exception as e:
        print(f"Error running dashboard: {e}")

def main():
    """Main function"""
    print("=" * 50)
    print("ACEH DEVELOPMENT DASHBOARD LAUNCHER")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("Please ensure all required files are present.")
        sys.exit(1)
    
    # Run dashboard
    run_dashboard()

if __name__ == "__main__":
    main()
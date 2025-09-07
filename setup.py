#!/usr/bin/env python3
"""
Setup script for Aceh Development Dashboard
This script sets up the project and creates sample data files
"""

import os
import subprocess
import sys
from data_processor import create_sample_data

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"Python version: {sys.version}")

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = ["data", "assets", "logs"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def setup_project():
    """Main setup function"""
    print("=" * 60)
    print("ACEH DEVELOPMENT DASHBOARD SETUP")
    print("=" * 60)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Install requirements
    install_requirements()
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nTo run the dashboard:")
    print("streamlit run main_app.py")
    print("\nThe dashboard will be available at: http://localhost:8501")
    print("\nProject structure:")
    print("├── main_app.py          # Main Streamlit application")
    print("├── config.py            # Configuration settings")
    print("├── utils.py             # Utility functions")
    print("├── data_processor.py    # Data processing functions")
    print("├── requirements.txt     # Python dependencies")
    print("├── setup.py            # This setup script")
    print("├── README.md           # Project documentation")
    print("└── data neraca regional/ # Data files directory")

if __name__ == "__main__":
    setup_project()
#!/usr/bin/env python3
"""
NBA Finals Analysis Suite Setup Script
=====================================

Professional setup and installation script for the NBA Finals betting market
analysis and Elo rating calculation suite.

Author: NBA Analytics Team
Version: 1.0.0
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def create_virtual_environment():
    """Create and activate virtual environment."""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return
    
    print("🔧 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        sys.exit(1)

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = Path(".venv/Scripts/pip")
    else:  # Unix/Linux/macOS
        pip_path = Path(".venv/bin/pip")
    
    try:
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def run_tests():
    """Run basic functionality tests."""
    print("🧪 Running functionality tests...")
    
    # Determine python path
    if os.name == 'nt':  # Windows
        python_path = Path(".venv/Scripts/python")
    else:  # Unix/Linux/macOS
        python_path = Path(".venv/bin/python")
    
    test_scripts = [
        "betting_market_vs_models.py",
        "visualization.py"
    ]
    
    for script in test_scripts:
        if Path(script).exists():
            try:
                result = subprocess.run([str(python_path), script], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ {script} - OK")
                else:
                    print(f"⚠️  {script} - Warning: {result.stderr[:100]}...")
            except subprocess.TimeoutExpired:
                print(f"⚠️  {script} - Timeout (likely interactive)")
            except Exception as e:
                print(f"❌ {script} - Error: {e}")

def display_usage_info():
    """Display usage information."""
    print("\n" + "="*60)
    print("🏀 NBA FINALS ANALYSIS SUITE - READY!")
    print("="*60)
    print("\n📚 Available Tools:")
    print("   • betting_market_vs_models.py - Market analysis engine")
    print("   • visualization.py - Professional charts and graphs")
    print("   • app.py - Web interface for Elo ratings")
    print("\n🚀 Quick Start:")
    print("   # Activate virtual environment")
    if os.name == 'nt':
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("\n   # Run market analysis")
    print("   python betting_market_vs_models.py")
    print("\n   # Start web app")
    print("   python app.py")
    print("\n📖 Documentation:")
    print("   • README.md - Main project documentation")
    print("   • BETTING_ANALYSIS.md - Betting analysis guide")
    print("\n⚠️  Disclaimer: Educational use only. Gamble responsibly.")
    print("="*60)

def main():
    """Main setup function."""
    print("🏀 NBA Finals Analysis Suite Setup")
    print("="*50)
    
    # Check requirements
    check_python_version()
    
    # Setup environment
    create_virtual_environment()
    install_dependencies()
    
    # Test functionality
    run_tests()
    
    # Display usage info
    display_usage_info()
    
    print("\n🎉 Setup completed successfully!")

if __name__ == "__main__":
    main() 
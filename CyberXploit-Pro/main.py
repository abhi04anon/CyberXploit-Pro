"""
CyberXploit Pro - Cross-Platform Cybersecurity Toolkit
Entry point for the application.
"""

import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import CyberXploitApp


def main():
    app = CyberXploitApp()
    app.run()


if __name__ == "__main__":
    main()

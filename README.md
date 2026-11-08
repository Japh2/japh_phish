# JAPHET Phish Framework

> **⚠️ DISCLAIMER: FOR EDUCATIONAL AND AUTHORIZED PENETRATION TESTING ONLY.**
> This tool was created as part of an academic project to understand the mechanics of phishing and credential harvesting. The author does not condone or support the use of this tool for illegal activities. Do not use this against targets you do not have explicit, written permission to test.

## Overview
**JAPHET Phish** is a lightweight, custom-built phishing simulation framework. It utilizes a Python Flask backend to serve a cloned login page and capture submitted credentials, logging them locally. 

## Features
- **Custom Frontend:** Serves a cloned Google login page (`index.html`).
- **Credential Capture:** Intercepts `POST` requests and logs emails/passwords to a local text file.
- **Automatic Redirection:** Redirects the victim to the real Google login page after submission to avoid suspicion.
- **Terminal Output:** Displays captured credentials in real-time via the terminal.
- **Ngrok Integration Ready:** Built to be easily tunneled to the public internet using Ngrok.

## Prerequisites
Before running this framework, ensure you have the following installed:
- Python 3
- Flask (`pip3 install Flask`)
- Ngrok (for public tunneling)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Japh2/japh_phish.git
   cd japh_phish
   sudo apt update
   sudo apt install python3-venv -y
   python3 -m venv myenv
   source myenv/bin/activate
   pip3 install Flask
   python3 evil_server.py

   

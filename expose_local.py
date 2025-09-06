#!/usr/bin/env python3
"""
Simple script to expose local Django server to internet using free tunneling services
"""
import subprocess
import sys
import requests
import json

def install_and_use_localtunnel():
    """Use localtunnel to expose the local server"""
    try:
        # Install localtunnel globally
        print("Installing localtunnel...")
        subprocess.run([sys.executable, "-m", "pip", "install", "localtunnel"], check=True)
        
        # Start localtunnel
        print("Starting localtunnel...")
        print("Your site will be available at a URL like: https://abc123.loca.lt")
        print("Press Ctrl+C to stop")
        
        subprocess.run(["npx", "localtunnel", "--port", "8000"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Make sure Node.js is installed on your system")
    except KeyboardInterrupt:
        print("\nTunnel stopped.")

def use_cloudflared():
    """Use Cloudflare tunnel (cloudflared)"""
    try:
        print("Downloading cloudflared...")
        # Download cloudflared for Windows
        import urllib.request
        import zipfile
        import os
        
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.zip"
        urllib.request.urlretrieve(url, "cloudflared.zip")
        
        with zipfile.ZipFile("cloudflared.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        os.remove("cloudflared.zip")
        
        print("Starting Cloudflare tunnel...")
        print("Your site will be available at a URL like: https://abc123.trycloudflare.com")
        print("Press Ctrl+C to stop")
        
        subprocess.run(["./cloudflared.exe", "tunnel", "--url", "http://localhost:8000"], check=True)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to start Cloudflare tunnel")

def main():
    print("🌐 Django Local Server Exposer")
    print("=" * 40)
    print("Options:")
    print("1. Use localtunnel (requires Node.js)")
    print("2. Use Cloudflare tunnel (cloudflared)")
    print("3. Manual instructions")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        install_and_use_localtunnel()
    elif choice == "2":
        use_cloudflared()
    elif choice == "3":
        print_manual_instructions()
    else:
        print("Invalid choice")

def print_manual_instructions():
    print("\n📋 Manual Instructions:")
    print("=" * 30)
    print("1. Download ngrok from: https://ngrok.com/download")
    print("2. Extract ngrok.exe to a folder")
    print("3. Open command prompt in that folder")
    print("4. Run: ngrok http 8000")
    print("5. Use the provided HTTPS URL")
    print("\nAlternative services:")
    print("- localtunnel: npm install -g localtunnel && localtunnel --port 8000")
    print("- serveo: ssh -R 80:localhost:8000 serveo.net")

if __name__ == "__main__":
    main()

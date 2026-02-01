"""
SETUP HELPER - Interactive configuration for the monitoring system
Run this to configure everything automatically
"""
import os
import sys
import json
from pathlib import Path

def print_header(text):
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50 + "\n")

def ask_question(question, default=""):
    response = input(f"❓ {question} [{default}]: ").strip()
    return response if response else default

def check_mongodb():
    print_header("MongoDB Configuration")
    print("MongoDB is needed to store data.")
    print("\nOptions:")
    print("1. Local MongoDB (Download from mongodb.com)")
    print("2. MongoDB Atlas (Cloud - Free tier)")
    
    choice = ask_question("Choose option (1 or 2)", "1")
    
    if choice == "2":
        connection_string = ask_question(
            "Enter MongoDB Atlas connection string",
            "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true"
        )
        return f'"{connection_string}"'
    else:
        host = ask_question("Enter MongoDB host", "localhost")
        port = ask_question("Enter MongoDB port", "27017")
        return f'"mongodb://{host}:{port}/"'

def setup_backend():
    print_header("Backend Server Configuration")
    
    backend_file = Path("backend.py")
    if not backend_file.exists():
        print("❌ backend.py not found!")
        return False
    
    mongo_uri = check_mongodb()
    
    # Read file
    with open(backend_file, 'r') as f:
        content = f.read()
    
    # Replace MongoDB URI
    content = content.replace(
        'MONGO_URI = "mongodb://localhost:27017/"',
        f'MONGO_URI = {mongo_uri}'
    )
    
    # Write back
    with open(backend_file, 'w') as f:
        f.write(content)
    
    print("✅ Backend configured successfully!")
    print(f"MongoDB URI set to: {mongo_uri}")
    
    return True

def setup_client():
    print_header("Client Configuration")
    
    client_file = Path("client.py")
    if not client_file.exists():
        print("❌ client.py not found!")
        return False
    
    backend_url = ask_question(
        "Enter backend server URL",
        "http://localhost:5000"
    )
    
    mongo_uri = check_mongodb()
    
    # Read file
    with open(client_file, 'r') as f:
        content = f.read()
    
    # Replace values
    content = content.replace(
        'BACKEND_URL = "http://localhost:5000"',
        f'BACKEND_URL = "{backend_url}"'
    )
    
    content = content.replace(
        'MONGO_URI = "mongodb://localhost:27017/"',
        f'MONGO_URI = {mongo_uri}'
    )
    
    # Write back
    with open(client_file, 'w') as f:
        f.write(content)
    
    print("✅ Client configured successfully!")
    print(f"Backend URL: {backend_url}")
    print(f"MongoDB URI: {mongo_uri}")
    
    return True

def install_dependencies():
    print_header("Installing Dependencies")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    print("Installing Python packages...")
    print("This may take a few minutes...\n")
    
    ret = os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    if ret == 0:
        print("\n✅ All dependencies installed!")
        return True
    else:
        print("\n❌ Failed to install dependencies!")
        return False

def create_config_file():
    print_header("Saving Configuration")
    
    config = {
        "backend": {
            "host": "0.0.0.0",
            "port": 5000,
            "debug": True
        },
        "client": {
            "poll_interval": 5,  # Check for commands every 5 seconds
        },
        "mongodb": {
            "database": "child_monitoring"
        }
    }
    
    with open("config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration saved to config.json")

def show_next_steps():
    print_header("SETUP COMPLETE! 🎉")
    print("""
Next Steps:

1️⃣  Start MongoDB:
    mongod

2️⃣  Run the Flask server:
    python backend.py
    
    ✅ You should see: "Running on http://127.0.0.1:5000"

3️⃣  Install client on child's computer:
    python client.py
    
    ✅ Check console for: "Device registered"

4️⃣  Open dashboard in browser:
    http://localhost:5000

5️⃣  Click on device to start monitoring!

📖 Read README.md for full documentation
🚀 Read QUICKSTART.md for quick reference

⚠️  IMPORTANT:
    - Keep backend.py running
    - Keep client.py running on child's PC
    - Keep MongoDB running (mongod)
    """)

def main():
    print("\n" + "="*50)
    print("  CHILD MONITORING SYSTEM - SETUP WIZARD")
    print("="*50)
    
    print("""
This wizard will help you configure the system.
It will ask a few questions and set everything up automatically.
    """)
    
    start = ask_question("Continue? (yes/no)", "yes")
    if start.lower() not in ["yes", "y", ""]:
        print("Setup cancelled!")
        return
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("Cannot continue without dependencies!")
        return
    
    # Step 2: Setup backend
    if not setup_backend():
        return
    
    # Step 3: Setup client
    if not setup_client():
        return
    
    # Step 4: Save config
    create_config_file()
    
    # Step 5: Show next steps
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled!")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()

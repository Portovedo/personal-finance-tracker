import os
import sys
import threading
import time
import uvicorn
import socket
import webview  # Import pywebview
from app.core.config import settings

# --- Working Directory Setup ---
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    sys.path.insert(0, sys._MEIPASS)
    os.chdir(application_path)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    # Make sure the backend directory is in the python path so 'app' is importable
    backend_dir = os.path.dirname(application_path) # e.g. .../backend
    sys.path.insert(0, backend_dir) 

# Port configuration
PORT = 8000
HOST = "127.0.0.1"

def start_server():
    """Runs the FastAPI server in a thread"""
    try:
        # Import app inside the thread to avoid blocking the main thread or causing circular imports early on
        from app.main import app
        uvicorn.run(app, host=HOST, port=PORT, log_level="error")
    except Exception as e:
        print(f"Server error: {e}")

def wait_for_server():
    """Wait until server accepts connections"""
    print("Waiting for server to start...")
    start = time.time()
    while time.time() - start < 10: # Wait up to 10 seconds
        try:
            with socket.create_connection((HOST, PORT), timeout=1):
                print("Server is up!")
                return True
        except (OSError, ConnectionRefusedError):
            time.sleep(0.5)
    return False

if __name__ == "__main__":
    # 1. Start Server Thread
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # 2. Wait for server to be ready
    if wait_for_server():
        # 3. Create Native Window
        webview.create_window(
            settings.PROJECT_NAME, 
            f"http://{HOST}:{PORT}",
            width=1200,
            height=800,
            resizable=True
        )
        # 4. Start GUI Loop
        webview.start()
    else:
        print("Error: Server failed to start or took too long.")
        # Ideally log the error or keep the console open briefly if needed
        input("Press Enter to exit...") 
        sys.exit(1)
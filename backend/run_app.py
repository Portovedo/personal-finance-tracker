import threading
import time
import socket
import uvicorn
import webview
from app.main import app

def get_free_port():
    """Finds an available port on the host machine."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

PORT = get_free_port()
HOST = "127.0.0.1"

def start_server():
    """Starts the FastAPI server on the discovered port."""
    uvicorn.run(app, host=HOST, port=PORT, log_level="error")

if __name__ == "__main__":
    # Start the API server in a separate thread
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # Allow a moment for the server to initialize
    time.sleep(0.5)

    # Launch the native desktop window
    webview.create_window(
        "Personal Finance Tracker",
        f"http://{HOST}:{PORT}",
        width=1200,
        height=800,
        resizable=True,
        text_select=True
    )

    webview.start()
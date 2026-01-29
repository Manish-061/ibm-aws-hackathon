import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app.api.routes import router
    print("Successfully imported router")
except Exception as e:
    print(f"Error importing router: {e}")

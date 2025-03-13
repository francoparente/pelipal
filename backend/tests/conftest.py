import os
import sys

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add backend/src to Python path
sys.path.insert(0, os.path.join(project_root, "backend", "src"))

# Print the paths for debugging
print(f"Project root: {project_root}")
print(f"Python path: {sys.path}")
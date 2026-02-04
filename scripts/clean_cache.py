import os
import shutil
from pathlib import Path

def clean():
    # Definišemo šta brišemo
    patterns = ["__pycache__", "*.pyc", "*.pyo", ".pytest_cache"]
    
    print("Cleaning cache files...")
    count = 0
    
    for pattern in patterns:
        for path in Path(".").rglob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                count += 1
            except Exception as e:
                print(f"Failed to delete {path}: {e}")
    
    print(f"Done! Removed {count} items.")

if __name__ == "__main__":
    clean()
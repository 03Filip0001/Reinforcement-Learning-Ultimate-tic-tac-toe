import os
import sys
import shutil
import subprocess

def main():
    goals = sys.argv[1:] 
    venv_dir = ".venv"

    if "delete" in goals:
        if os.path.exists(venv_dir):
            shutil.rmtree(venv_dir)
            print("Virtual environment deleted.")
        return

    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir])
        
        pip_venv = None
        python_venv = None
        if os.name == "nt":
            pip_venv = os.path.join(venv_dir, "Scripts", "pip")
            python_venv = os.path.join(venv_dir, "Scripts", "python.exe")
        else:
            pip_venv = os.path.join(venv_dir, "bin", "pip")
            python_venv = os.path.join(venv_dir, "bin", "python")

        if python_venv is not None:
            print("Updating pip...")
            subprocess.run([python_venv, "-m", "pip", "install", "--upgrade", "pip"])
        else:
            print("ERROR creating venv environment !")
            return
        
        if os.path.exists("requirements.txt"):
            print("Installing packages...")
            subprocess.run([pip_venv, "install", "-r", "requirements.txt"])
        else:
            print("ERROR installing packages !")
    else:
        print("Environment already exists.")

if __name__ == "__main__":
    main()
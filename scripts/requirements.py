import os
import subprocess

def main():
	venv_dir = ".venv"
	pip_venv = os.path.join(venv_dir, "Scripts", "pip")
	if os.path.exists("requirements.txt"):
		print("Installing packages...")
		subprocess.run([pip_venv, "install", "-r", "requirements.txt"])
	else:
		print("ERROR installing packages !")

if __name__ == "__main__":
	main()
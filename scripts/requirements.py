import os
import subprocess

def main():
	venv_dir = ".venv"
	pip_venv = None
	if os.name == "nt":
		pip_venv = os.path.join(venv_dir, "Scripts", "pip")
	else:
		pip_venv = os.path.join(venv_dir, "bin", "pip")

	if os.path.exists("requirements.txt"):
		print("Installing packages...")
		subprocess.run([pip_venv, "install", "--no-cache-dir", "-r", "requirements.txt"])
	else:
		print("ERROR installing packages !")

if __name__ == "__main__":
	main()
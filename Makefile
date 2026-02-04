.DEFAULT_GOAL := run

ifeq ($(OS),Windows_NT)
    VENV_PYTHON = .venv\Scripts\python.exe
else
    VENV_PYTHON = .venv/bin/python
endif

.PHONY: environment run clean delete

run: environment
	@$(VENV_PYTHON) main.py

environment:
	@python scripts/setup_env.py $(MAKECMDGOALS)

clean:
	@python scripts/clean_cache.py

delete:
	@:
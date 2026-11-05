MAKEFLAGS := --silent
NAME := a_maze_ing.py
VENV := venv
LOCAL_PY := python3
DEBUG := -m pdb
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy

SRC := a_maze_ing

all: $(VENV)

$(VENV):
	if [ ! -d "$(VENV)" ]; then \
		$(LOCAL_PY) -m venv $(VENV); \
		$(PIP) install --upgrade pip; \
		$(PIP) install flake8 mypy; \
		echo "Ambiente virtual criado com sucesso!"; \
	else \
		echo "Ambiente virtual ja criado!"; \
	fi

install:
	if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "Dependencias nao encontradas"; \
	fi

run:
	$(PY) a_maze_ing/$(NAME)

debug:
	$(PY) $(DEBUG) a_maze_ing/$(NAME)

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	echo "cache e ambiente virtual removidos!"

lint:
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude $(VENV)

lint-strict:
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . --strict --exclude $(VENV)

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

# Permite passar argumentos diretamente (ex: make run config.txt ou make run ARGS=config.txt)
ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

ARGS ?= $(RUN_ARGS)

run:
	-$(PY) a_maze_ing/$(NAME) $(ARGS)

debug:
	$(PY) $(DEBUG) a_maze_ing/$(NAME) $(ARGS)

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
	$(MYPY) . --warn-unused-configs --disallow-any-generics --disallow-subclassing-any --disallow-incomplete-defs --check-untyped-defs --disallow-untyped-decorators --no-implicit-optional --warn-redundant-casts --warn-unused-ignores --warn-return-any --no-implicit-reexport --strict-equality --extra-checks --ignore-missing-imports --exclude $(VENV)

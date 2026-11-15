MAKEFLAGS := --silent
NAME := a_maze_ing.py
PACKAGE := mazegen
VENV := venv
LOCAL_PY := python3
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy

.PHONY: all install run debug package clean fclean re lint lint-strict

all: $(VENV)

$(VENV):
	if [ ! -d "$(VENV)" ]; then \
		$(LOCAL_PY) -m venv $(VENV); \
		$(PIP) install --upgrade pip; \
		$(PIP) install flake8 mypy; \
		echo "Virtual environment created successfully!"; \
	else \
		echo "Virtual environment already created!"; \
	fi

install: $(VENV)
	$(PIP) install -e .

# Permite passar argumentos diretamente (ex: make run config.txt)
ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
ifeq (debug,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

ARGS ?= $(RUN_ARGS)

run:
	-$(PY) $(NAME) $(ARGS)

debug:
	$(PY) -m pdb $(NAME) $(ARGS)

package: $(VENV)
	$(PIP) install --quiet build
	$(PY) -m build
	cp dist/$(PACKAGE)-*.whl .
	echo "Package built: $(PACKAGE)-*.whl"

clean:
	find . -type d \( -name __pycache__ -o -name .mypy_cache \) -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	echo "Cache removed!"

fclean: clean
	rm -rf $(VENV) build dist *.egg-info
	echo "Virtual environment and build artifacts removed!"

re: fclean all

lint:
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude $(VENV)

lint-strict:
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . --strict --ignore-missing-imports --exclude $(VENV)

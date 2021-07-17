prod:
	DISPLAY=":0" \
	poetry run python3 main.py

prod-cProfile:
	DISPLAY=":0" \
	poetry run python3 -m cProfile -s tottime main.py > log/cProfile_`date +%Y%m%d_%H%M%S`.log

debug:
	DEBUG=TRUE \
	poetry run python3 main.py

debug-cProfile:
	DEBUG=TRUE \
	poetry run python3 -m cProfile -s tottime main.py > log/cProfile_`date +%Y%m%d_%H%M%S`.log

format:
	poetry run yapf -i --recursive ./src

type-check:
	poetry run mypy -p src

test:
	poetry run python -m pytest

lint:
	poetry run flake8 ./src
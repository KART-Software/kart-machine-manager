prod:
	DISPLAY=":0" \
	pipenv run python3 main.py

prod-cProfile:
	DISPLAY=":0" \
	pipenv run python3 -m cProfile -s tottime main.py > log/cProfile_`date +%Y%m%d_%H%M%S`.log

debug:
	DEBUG=TRUE \
	pipenv run python3 main.py

debug-cProfile:
	DEBUG=TRUE \
	pipenv run python3 -m cProfile -s tottime main.py > log/cProfile_`date +%Y%m%d_%H%M%S`.log

format:
	pipenv run yapf -i --recursive ./src

type-check:
	pipenv run mypy -p src

test:
	pipenv run python -m pytest

lint:
	pipenv run flake8 ./src
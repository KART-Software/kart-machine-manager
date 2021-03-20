prod:
	DISPLAY=":0" \
	pipenv run python3 main.py

debug:
	DEBUG=TRUE \
	pipenv run python3 main.py

format:
	pipenv run yapf -i --recursive ./src

type-check:
	pipenv run mypy -p src

test:
	pipenv run python -m pytest

lint:
	pipenv run flake8 ./src
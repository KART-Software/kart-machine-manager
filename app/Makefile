prod:
	DEBUG=FALSE
	DISPLAY=":0" \
	rye run python main.py

debug:
	DEBUG=TRUE \
	rye run python main.py

format:
	rye run ruff format

lint:
	rye run ruff check

lint-fix:
	rye run ruff check --fix

type-check:
	rye run mypy .

test:
	rye test

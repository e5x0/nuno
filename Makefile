SHELL=/bin/bash
.PHONY: pre
pre:
	. .venv/bin/activate \
	&& rye sync \
	&& pre-commit install

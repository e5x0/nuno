.PHONY: pre
pre:
	rye sync
	pre-commit install
 
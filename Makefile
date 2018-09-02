.PHONY: help
	@echo "Available targets:"
	@echo "    lint"
	@echo "    help"


.PHONY: lint
lint:
	python -m flake8 .

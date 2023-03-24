.PHONY: test release

test:
	@bash ./scripts/test.sh

lint:
	 @bash ./scripts/lint.sh

format:
	@bash ./scripts/format.sh

release:
	python3 -m build
	python3 -m twine upload dist/*


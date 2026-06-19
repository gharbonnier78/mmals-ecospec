.PHONY: test demo paper clean

test:
	python -m pytest

demo:
	python examples/toy_demo.py

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	cd paper && latexmk -C
	rm -rf artifacts .pytest_cache

.PHONY: install build test clean

install:
	pip install -r requirements.txt

build:
	python scripts/generate.py
	python scripts/compile_pdf.py

test:
	pytest -q || test $$? -eq 5

clean:
	rm -rf output pdf_output logs

.PHONY: check pdf pdf-monografia release-check
check:
	python3 scripts/verificar.py
	python3 -m unittest discover -s tests -v
pdf:
	mkdir -p build
	cd monografia && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
pdf-monografia:
	mkdir -p build
	cd monografia && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build monografia.tex
release-check:
	python3 scripts/verificar.py --release

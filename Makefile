.PHONY: check pdf pdf-en pdf-monografia release-check site site-servir
check:
	python3 scripts/verificar.py
	python3 scripts/verificar_traducao.py
	python3 -m unittest discover -s tests -v
# Artigo no formato SBC Reviews: a classe da revista exige LuaLaTeX ou XeLaTeX.
pdf:
	mkdir -p build
	cd monografia && latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=../build main.tex
pdf-en:
	mkdir -p build
	cd monografia && latexmk -lualatex -interaction=nonstopmode -halt-on-error -outdir=../build main-en.tex
pdf-monografia:
	mkdir -p build
	cd monografia && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build monografia.tex
release-check:
	python3 scripts/verificar.py --release
site:
	python3 scripts/gerar_site.py
site-servir:
	python3 -m http.server 8765 --bind 127.0.0.1 --directory site

# \ var
MODULE  = $(notdir $(CURDIR))
OS      = $(shell uname -s)
MACHINE = $(shell uname -m)
NOW     = $(shell date +%d%m%y)
REL     = $(shell git rev-parse --short=4 HEAD)
CORES   = $(shell grep processor /proc/cpuinfo| wc -l)
# / var

# \ dir
CWD     = $(CURDIR)
BIN     = $(CWD)/bin
DOC     = $(CWD)/doc
TMP     = $(CWD)/tmp
LIB     = $(CWD)/lib
SRC     = $(CWD)/src
TEST    = $(CWD)/test
GZ      = $(HOME)/gz
# / dir

# \ tool
CURL    = curl -L -o
PY      = bin/python3
PIP     = bin/pip3
PEP     = bin/autopep8
PYT     = bin/pytest
TEX     = pdflatex -shell-escape -halt-on-error -output-directory=$(TMP)
# / tool

# \ src
P      += config.py
Y      += metaL.py test_metaL.py
T      += doc/book.tex
T      += $(shell find doc -type f -regex ".+.tex$$")
TS     += $(shell find doc -type f -regex ".+.py$$")
TS     += $(shell find doc -type f -regex ".+.txt$$")
TS     += $(shell find doc -type f -regex ".+.html$$")
TI     += $(shell find doc -type f -regex ".+.png$$")
TI     += $(shell find doc -type f -regex ".+.jpeg$$")
TI     += $(shell find doc -type f -regex ".+.jpg$$")
S      += $(Y) $(T) $(TS) $(TI)
# / src

# \ all
all: $(PY) metaL.py
	$^ $@
	$(MAKE) test
web: $(PY) metaL.py
	$^ $@
	$(MAKE) test
repl: $(PY) metaL.py
	$^ $@
	$(MAKE) test
.PHONY: test
test: $(PYT) test_metaL.py
	$^
	$(MAKE) format
.PHONY: format
format: $(PEP)
$(PEP): $(Y)
	$@ --ignore=E26,E302,E401,E402,E701,E702 --in-place $? && touch $@
# / all

# \ tex
.PHONY: tex
tex: tmp/$(MODULE).pdf
tmp/$(MODULE).pdf: $(T) $(TS) $(TI)
#	$(TEX) $< && $(TEX) $<
	$(TEX) $< |tail -n5 && $(TEX) $< |tail -n5
.PHONY: pdf
pdf: tmp/metaL_$(REL)_$(NOW).pdf
tmp/metaL_$(REL)_$(NOW).pdf: tmp/$(MODULE).pdf
#	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen \
#		-dNOPAUSE -dQUIET -dBATCH -sOutputFile=$@ $<
	cp $< $@
	cp $@ doc/metaL.pdf
# / tex

# / doc
doc: \
	doc/SICP_ru.pdf doc/Dragon_ru.pdf \
	doc/Erlang/LYSE_ru.pdf doc/Erlang/Armstrong_ru.pdf doc/Erlang/ElixirInAction.pdf \
	doc/NimInAction.pdf doc/Python_ru.pdf

doc/SICP_ru.pdf:
	$(CURL) $@ https://newstar.rinet.ru/~goga/sicp/sicp.pdf
doc/Dragon_ru.pdf:
	$(CURL) $@ https://linux-doc.ru/programming/assembler/book/compilers.pdf

doc/Erlang/LYSE_ru.pdf:
	$(CURL) $@ https://github.com/mpyrozhok/learnyousomeerlang_ru/raw/master/pdf/learnyousomeerlang_ru.pdf
doc/Erlang/Armstrong_ru.pdf:
	$(CURL) $@ https://github.com/dyp2000/Russian-Armstrong-Erlang/raw/master/pdf/fullbook.pdf
doc/Erlang/ElixirInAction.pdf:
	$(CURL) $@ https://github.com/levunguyen/CGDN-Ebooks/raw/master/Java/Elixir%20in%20Action%2C%202nd%20Edition.pdf

doc/NimInAction.pdf:
	$(CURL) $@ https://nim.nosdn.127.net/MTY3NjMzODI=/bmltd18wXzE1NzYxNTc0NDQwMTdfMWU4MDhiODUtZDM0Ni00OWFlLWJjYzUtMDg2ODIxMmMzMTIw
doc/Python_ru.pdf:
	$(CURL) $@ http://rus-linux.net/MyLDP/BOOKS/python.pdf
# / doc

# \ install
.PHONY: install
install: $(OS)_install js doc
	$(MAKE) $(PIP)
	$(MAKE) update
.PHONY: update
update: $(OS)_update
	$(PIP) install -U    pip autopep8
	$(PIP) install -U -r requirements.txt

.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt apt.dev`

# \ py
$(PY) $(PIP):
	python3 -m venv .
	$(MAKE) update
$(PYT):
	$(PIP) install -U pytest
# / py

# \ js
.PHONY: js
js:
js: \
	static/js/bootstrap.min.css static/js/bootstrap.dark.css \
	static/js/bootstrap.min.js  static/js/jquery.min.js \
	static/js/html5shiv.min.js  static/js/respond.min.js \
	static/js/socket.io.min.js  static/js/peg.min.js \
	static/js/Lato.font.css

CDNJS = https://cdnjs.cloudflare.com/ajax/libs

JQUERY_VER = 3.6.0
static/js/jquery.min.js:
	$(CURL) $@ $(CDNJS)/jquery/$(JQUERY_VER)/jquery.min.js

BOOTSTRAP_VER = 4.6.0
BOOTSTRAP_CDN = $(CDNJS)/twitter-bootstrap/$(BOOTSTRAP_VER)
static/js/bootstrap.min.css: static/js/bootstrap.min.css.map
	$(CURL) $@ $(BOOTSTRAP_CDN)/css/bootstrap.min.css
static/js/bootstrap.min.css.map:
	$(CURL) $@ $(BOOTSTRAP_CDN)/css/bootstrap.min.css.map
static/js/bootstrap.dark.css:
	$(CURL) $@ https://bootswatch.com/4/darkly/bootstrap.min.css
	sed -E "s/https:\/\/fonts.+=swap/\/static\/js\/Lato.font.css/" -i $@
static/js/bootstrap.min.js: static/js/bootstrap.min.js.map
	$(CURL) $@ $(BOOTSTRAP_CDN)/js/bootstrap.min.js
static/js/bootstrap.min.js.map:
	$(CURL) $@ $(BOOTSTRAP_CDN)/js/bootstrap.min.js.map

static/js/html5shiv.min.js:
	$(CURL) $@ $(CDNJS)/html5shiv/3.7.3/html5shiv.min.js
static/js/respond.min.js:
	$(CURL) $@ $(CDNJS)/respond.js/1.4.2/respond.min.js

static/js/Lato.font.css:
	$(CURL) $@ "https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400&display=swap"

SOCKETIO_VER = 3.1.2
SOCKETIO_CDN = $(CDNJS)/socket.io/$(SOCKETIO_VER)
static/js/socket.io.min.js: static/js/socket.io.min.js.map
	$(CURL) $@ $(SOCKETIO_CDN)/socket.io.min.js
static/js/socket.io.min.js.map:
	$(CURL) $@ $(SOCKETIO_CDN)/socket.io.min.js.map

PEGJS_VER = 0.10.0
static/js/peg.min.js:
	$(CURL) $@ https://github.com/pegjs/pegjs/releases/download/v$(PEGJS_VER)/peg-$(PEGJS_VER).min.js

# / install

# \ merge
MERGE += README.md Makefile .gitignore apt.txt apt.dev LICENSE $(S)
MERGE += .vscode bin doc tmp src test
MERGE += requirements.txt
MERGE += static templates

.PHONY: main
main:
	git push -v
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)
.PHONY: shadow
shadow:
	git push -v
	git checkout $@
	git pull -v
.PHONY: release
release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) pdf
	$(MAKE) shadow
.PHONY: zip
zip:
	git archive \
		--format zip \
		--output $(TMP)/$(MODULE)_$(NOW)_$(REL).src.zip \
	HEAD
# / merge

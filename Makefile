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
T      += doc/book.tex doc/header.tex doc/title.tex doc/contacts.tex
T      += doc/intro/intro.tex doc/intro/meta.tex doc/intro/install.tex
T      += doc/intro/ast.tex doc/intro/krr.tex doc/intro/eds.tex
T      += doc/core/core.tex doc/core/object.tex doc/core/graph.tex
TY     += doc/core/object0.py
T      += doc/bib/bib.tex
S      += $(Y) $(T)
# / src

# \ all
all: $(PY) metaL.py
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
tmp/$(MODULE).pdf: $(T) $(TY)
#	$(TEX) $< && $(TEX) $<
	$(TEX) $< |tail -n5 && $(TEX) $< |tail -n5
.PHONY: pdf
pdf: tmp/metaL_$(REL)_$(NOW).pdf
tmp/metaL_$(REL)_$(NOW).pdf: tmp/$(MODULE).pdf
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen \
		-dNOPAUSE -dQUIET -dBATCH -sOutputFile=$@ $<
	cp $@ doc/metaL.pdf
# / tex

# / doc
doc: \
	doc/SICP_ru.pdf
doc/SICP_ru.pdf:
	$(CURL) $@ https://newstar.rinet.ru/~goga/sicp/sicp.pdf
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
	$(MAKE) shadow
.PHONY: zip
zip:
	git archive \
		--format zip \
		--output $(TMP)/$(MODULE)_$(NOW)_$(REL).src.zip \
	HEAD
# / merge

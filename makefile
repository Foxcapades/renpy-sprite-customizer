VERSION := $(shell grep 'define config.version' game/options.rpy | sed 's/.\+"\(.\+\)"/\1/')
FEATURE := $(shell grep 'define config.version' game/options.rpy | sed 's/.\+"\(.\+\)"/\1/;s/\([0-9]\+\.[0-9]\+\).\+/\1.0/')

.PHONY: default
default:
	@echo "What are you doing?"


.PHONY: clean
clean:
	@find . -name '*.rpyc' | xargs -I'{}' rm {}


.PHONY: build-src-release
build-src-release: clean
	@mkdir -p releases
	@zip -r "releases/base-project-$(VERSION).zip" game license -x game/saves/**\*


.PHONY: build-docs
build-docs:
	@mkdir -p docs/versions/$(FEATURE)
	@asciidoctor -b html5 -o docs/index.html -a revnumber=$(FEATURE) docs/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/index.html -a revnumber=$(FEATURE) docs/reference/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/tutorial.html -a revnumber=$(FEATURE) docs/reference/tutorial.adoc
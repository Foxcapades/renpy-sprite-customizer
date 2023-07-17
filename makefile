VERSION := $(shell grep 'define config.version' game/options.rpy | sed 's/.\+"\(.\+\)"/\1/')

.PHONY: default
default:
	@echo "What are you doing?"

.PHONY: build-src-release
build-src-release:
	@mkdir -p releases
	@zip -r "releases/base-project-$(VERSION).zip" game license -x game/saves/**\*

.PHONY: build-docs
build-docs:
	@mkdir -p docs/versions/$(VERSION)
	@asciidoctor -b html5 -o docs/index.html -a revnumber=$(VERSION) docs/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(VERSION)/index.html -a revnumber=$(VERSION) docs/reference/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(VERSION)/tutorial.html -a revnumber=$(VERSION) docs/reference/tutorial.adoc
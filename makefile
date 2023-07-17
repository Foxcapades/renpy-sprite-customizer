VERSION := "1.0.1"
FEATURE := "1.0.0"

.PHONY: default
default:
	@echo "What are you doing?"

.PHONY: build-src-release
build-src-release:
	@mkdir -p releases
	@zip -r "releases/base-project-$(VERSION).zip" game license -x game/saves/**\*

.PHONY: build-docs
build-docs:
	@mkdir -p docs/versions/$(FEATURE)
	@asciidoctor -b html5 -o docs/index.html -a revnumber=$(FEATURE) docs/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/index.html -a revnumber=$(FEATURE) docs/reference/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/tutorial.html -a revnumber=$(FEATURE) docs/reference/tutorial.adoc
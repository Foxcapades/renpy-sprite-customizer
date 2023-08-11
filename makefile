VERSION := $(shell grep 'define config.version' game/options.rpy | sed 's/.\+"\(.\+\)"/\1/')
FEATURE := $(shell grep 'define config.version' game/options.rpy | sed 's/.\+"\(.\+\)"/\1/;s/\([0-9]\+\.[0-9]\+\).\+/\1.0/')

SLIM_ZIP_NAME := "build/sc-slim-$(VERSION).zip"
FULL_ZIP_NAME := "build/sc-project-$(VERSION).zip"

.PHONY: default
default:
	@echo "What are you doing?"


.PHONY: clean
clean:
	@echo "Cleaning directory."
	@find . -name '*.rpyc' -o -name '*.rpyb' -o -name '*.rpymc' | xargs -I'{}' rm '{}'


.PHONY: release
release: build-base-project-zip build-slim-zip


.PHONY: build-base-project-zip
build-base-project-zip: clean
	@mkdir -p build
	@rm -f "$(FULL_ZIP_NAME)"
	@cp license sc-license
	@zip -r "$(FULL_ZIP_NAME)" game sc-license -x game/saves/**\* -x game/cache/**\*
	@rm sc-license


.PHONY: build-slim-zip
build-slim-zip: clean
	@mkdir -p build
	@rm -f "$(SLIM_ZIP_NAME)"
	@cp license sc-license
	@zip -r "$(SLIM_ZIP_NAME)" game/lib/fxcpds/sprite_customizer sc-license
	@rm sc-license


.PHONY: docs
docs:
	@mkdir -p docs/versions/$(FEATURE)
	@asciidoctor -b html5 -o docs/index.html -a revnumber=$(FEATURE) docs/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/index.html -a revnumber=$(FEATURE) docs/reference/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/tutorial.html -a revnumber=$(FEATURE) docs/reference/tutorial.adoc
VERSION := $(shell grep 'define config.version' game/options.rpy | sed 's/.\+"\(.\+\)"/\1/')
FEATURE := $(shell grep 'define config.version' game/options.rpy | sed 's/.\+"\(.\+\)"/\1/;s/\([0-9]\+\.[0-9]\+\).\+/\1.0/')

.PHONY: default
default:
	@echo "What are you doing?"


.PHONY: clean
clean:
	@find . -name '*.rpyc' | xargs -I'{}' rm {}


.PHONY: release
release: build-base-project-zip build-slim-zip


.PHONY: build-base-project-zip
build-base-project-zip: clean
	@mkdir -p releases
	@zip -r "releases/sc-base-project-$(VERSION).zip" game license -x game/saves/**\*


.PHONY: build-slim-zip
build-slim-zip: clean
	@mkdir -p releases
	@zip -r "releases/sc-slim-$(VERSION).zip" game/lib/fxcpds/sprite_customizer game/customized_sprites.rpy license


.PHONY: docs
docs:
	@mkdir -p docs/versions/$(FEATURE)
	@asciidoctor -b html5 -o docs/index.html -a revnumber=$(FEATURE) docs/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/index.html -a revnumber=$(FEATURE) docs/reference/index.adoc
	@asciidoctor -b html5 -o docs/versions/$(FEATURE)/tutorial.html -a revnumber=$(FEATURE) docs/reference/tutorial.adoc
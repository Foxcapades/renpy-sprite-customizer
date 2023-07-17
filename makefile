GIT_TAG := $(shell git describe --tags)

.PHONY: default
default:
	@echo "What are you doing?"

.PHONY: build-src-release
build-src-release:
	@mkdir -p releases
	@zip -r "releases/base-project-$(GIT_TAG).zip" game license -x game/saves/**\*

.PHONY: build-docs
build-docs:
	@asciidoctor -b html5 -o docs/index.html docs/index.adoc
	@asciidoctor -b html5 -o docs/docs/tutorial.html docs/docs/tutorial.adoc